#

"""Tox plugin hooks."""

import pathlib
import typing

import poetry.core.factory
import tomlkit
import tox

if typing.TYPE_CHECKING:
    IndexServersT = typing.Tuple[
        tox.config.IndexServerConfig,  # PIP_INDEX_URL
        typing.List[tox.config.IndexServerConfig],  # PIP_EXTRA_INDEX_URL
    ]

PIP_DEFAULT_INDEX_SERVER_URL = 'https://pypi.org/simple'
PIP_DEFAULT_INDEX_SERVER_NAME = 'pypi'

POETRY_LOCKFILE_FILE_NAME = 'poetry.lock'


class _Exception(Exception):
    """Base exception."""


class NoPoetryFound(_Exception):
    """No poetry found."""


class NoPyprojectTomlFound(_Exception):
    """No 'pyproject.toml' file  found."""


class CanNotHaveMultipleDefaultSourceRepositories(_Exception):
    """Can not have multiple 'default' source repositories."""


@tox.hookimpl  # type: ignore[misc]
def tox_addoption(parser: tox.config.Parser) -> None:
    """Set hook."""
    parser.add_testenv_attribute(
        'add_poetry_dev_dependencies',
        'bool',
        "Add Poetry's 'dev-dependencies' to the test environment.",
        default=False,
    )
    parser.add_testenv_attribute(
        'poetry_use_source_repos',
        'string',
        (
            "Use Poetry's source repositories. Set 'pip_env_vars' to set as"
            " Pip environment variables ('PIP_INDEX_URL' and"
            " 'PIP_EXTRA_INDEX_URL')."
        ),
    )
    parser.add_testenv_attribute(
        'poetry_experimental_no_virtual_env',
        'bool',
        "(EXPERIMENTAL) Do not create a virtual environment.",
        default=False,
    )
    parser.add_testenv_attribute(
        'poetry_experimental_add_locked_dependencies',
        'bool',
        (
            "(EXPERIMENTAL) Add Poetry's locked dependencies from the lockfile"
            " to 'deps' in the test environment."
        ),
        default=False,
    )


def _is_test_env(env_config: tox.config.TestenvConfig) -> bool:
    """Check if it is a test environment.

    Tox creates environments for provisioning (`.tox`) and for isolated build
    (`.packaging`) in addition to the usual test environments. And in hooks
    such as `tox_testenv_create` it is not clear if the environment is a test
    environment or one of those environments used for tox's own purposes.

    So we start by excluding the provisioning environment named after
    `provision_tox_env` and the build isolation environment named after
    `isolated_build_env`. Then we keep only the environments listed in
    `envlist`.
    """
    #
    is_test_env = False
    #
    tox_config = env_config.config
    env_name = env_config.envname
    #
    known_private_env_names = []
    #
    provision_tox_env = getattr(tox_config, 'provision_tox_env', None)
    if provision_tox_env:
        known_private_env_names.append(provision_tox_env)
    #
    isolated_build_env = getattr(tox_config, 'isolated_build_env', None)
    if isolated_build_env:
        known_private_env_names.append(isolated_build_env)
    #
    if env_name not in known_private_env_names:
        if env_name in tox_config.envlist:
            is_test_env = True
    #
    return is_test_env


@tox.hookimpl  # type: ignore[misc]
def tox_configure(config: tox.config.Config) -> None:
    """Set hook."""
    #
    project_dir_path = pathlib.Path(config.setupdir)
    #
    try:
        poetry_ = _get_poetry(project_dir_path)
    except (NoPoetryFound, NoPyprojectTomlFound):
        pass
    else:
        #
        locked_deps = _get_locked_deps(project_dir_path)
        _add_locked_dependencies(config, locked_deps)
        #
        dev_deps = _get_dev_requirements(poetry_)
        _add_dev_dependencies(config, dev_deps)
        #
        index_servers = _get_index_servers(poetry_)
        _add_index_servers(config, index_servers)


@tox.hookimpl  # type: ignore[misc]
def tox_testenv_create(
        venv: tox.venv.VirtualEnv,
        action: tox.action.Action,  # pylint: disable=unused-argument
) -> typing.Any:
    """Set hook."""
    #
    result = None
    #
    if _is_test_env(venv.envconfig):
        if venv.envconfig.poetry_experimental_no_virtual_env is True:
            #
            tox.venv.cleanup_for_venv(venv)
            #
            python_link_name = venv.envconfig.get_envpython()
            python_link_path = pathlib.Path(python_link_name)
            python_link_path.parent.mkdir(parents=True)
            python_link_target = (
                tox.interpreters.tox_get_python_executable(venv.envconfig)
            )
            pathlib.Path(python_link_name).symlink_to(python_link_target)
            #
            result = True  # anything but None
    #
    return result


def _add_dev_dependencies(
        tox_config: tox.config.Config,
        dev_dep_configs: typing.Iterable[tox.config.DepConfig],
) -> None:
    #
    for env_config in tox_config.envconfigs.values():
        if env_config.poetry_experimental_add_locked_dependencies is not True:
            if _is_test_env(env_config):
                if env_config.add_poetry_dev_dependencies is True:
                    for dep_config in dev_dep_configs:
                        env_config.deps.append(dep_config)


def _add_index_servers(
        tox_config: tox.config.Config,
        index_servers: 'IndexServersT',
) -> None:
    #
    for env_config in tox_config.envconfigs.values():
        if env_config.poetry_use_source_repos == 'pip_env_vars':
            _add_index_servers_as_pip_env_vars(env_config, index_servers)


def _add_index_servers_as_pip_env_vars(
        env_config: tox.config.TestenvConfig,
        index_servers: 'IndexServersT',
) -> None:
    #
    pip_index_server = index_servers[0]
    pip_extra_index_servers = index_servers[1]
    #
    env_vars = env_config.setenv
    #
    if env_vars.get('PIP_INDEX_URL') is None and pip_index_server:
        env_vars['PIP_INDEX_URL'] = pip_index_server.url
    #
    if env_vars.get('PIP_EXTRA_INDEX_URL') is None and pip_extra_index_servers:
        env_config.setenv['PIP_EXTRA_INDEX_URL'] = ' '.join(
            [index_server.url for index_server in pip_extra_index_servers],
        )


def _add_locked_dependencies(
        tox_config: tox.config.Config,
        locked_deps: typing.Mapping[str, typing.List[tox.config.DepConfig]],
) -> None:
    #
    for env_config in tox_config.envconfigs.values():
        if _is_test_env(env_config):
            if env_config.poetry_experimental_add_locked_dependencies is True:
                for dep_config in locked_deps['main']:
                    env_config.deps.append(dep_config)
                if env_config.add_poetry_dev_dependencies is True:
                    for dep_config in locked_deps['dev']:
                        env_config.deps.append(dep_config)


def _get_poetry(project_root_path: pathlib.Path) -> poetry.core.poetry.Poetry:
    poetry_factory = poetry.core.factory.Factory()
    try:
        poetry_ = poetry_factory.create_poetry(str(project_root_path))
    except RuntimeError as exc:
        raise NoPyprojectTomlFound from exc
    except poetry.core.pyproject.exceptions.PyProjectException as exc:
        raise NoPoetryFound from exc
    return poetry_


def _get_dev_requirements(
        poetry_: poetry.core.poetry.Poetry,
) -> typing.List[tox.config.DepConfig]:
    #
    requirements = [
        tox.config.DepConfig(dependency.to_pep_508())
        for dependency in poetry_.package.dev_requires
    ]
    return requirements


def _get_index_servers(
        poetry_: poetry.core.poetry.Poetry,
) -> 'IndexServersT':
    #
    poetry_source_repos = poetry_.local_config.get('source', [])
    #
    poetry_default_server = None
    poetry_normal_servers = []
    poetry_secondary_servers = []
    #
    for poetry_source_repo in poetry_source_repos:
        server = tox.config.IndexServerConfig(
            poetry_source_repo['name'],
            poetry_source_repo['url'],
        )
        #
        if poetry_source_repo.get('default', False) is True:
            if poetry_default_server is None:
                poetry_default_server = server
            else:
                raise CanNotHaveMultipleDefaultSourceRepositories
            #
        elif poetry_source_repo.get('secondary', False) is True:
            poetry_secondary_servers.append(server)
        else:
            poetry_normal_servers.append(server)
    #
    pip_index_server = None
    pip_extra_index_servers = []
    #
    if poetry_default_server:
        pip_index_server = poetry_default_server
    elif poetry_normal_servers:
        pip_index_server = poetry_normal_servers.pop(0)
    #
    pip_extra_index_servers.extend(poetry_normal_servers)
    #
    if pip_index_server:
        # Pip's default index (PyPI) is not the default anymore, so it needs to
        # be inserted again right before the secondary indexes.
        pip_default_index_server = tox.config.IndexServerConfig(
            PIP_DEFAULT_INDEX_SERVER_NAME,
            PIP_DEFAULT_INDEX_SERVER_URL,
        )
        pip_extra_index_servers.append(pip_default_index_server)
    #
    pip_extra_index_servers.extend(poetry_secondary_servers)
    #
    index_servers = (
        pip_index_server,
        pip_extra_index_servers,
    )
    #
    return index_servers


def _get_locked_deps(
        project_root_path: pathlib.Path,
) -> typing.Dict[str, typing.List[tox.config.DepConfig]]:
    #
    locked_deps: typing.Dict[str, typing.List[tox.config.DepConfig]] = {}
    #
    lock_file_path = project_root_path.joinpath(POETRY_LOCKFILE_FILE_NAME)
    if lock_file_path.is_file():
        #
        lock_str = lock_file_path.read_text()
        lock_document = tomlkit.parse(lock_str)
        #
        for dependency in lock_document['package']:
            #
            dep_name = dependency['name']
            dep_version = dependency['version']
            #
            dep_pep_508 = f'{dep_name}=={dep_version}'
            #
            dep_category = dependency['category']
            dep_config = tox.config.DepConfig(dep_pep_508)
            locked_deps.setdefault(dep_category, []).append(dep_config)
    #
    return locked_deps


# EOF
