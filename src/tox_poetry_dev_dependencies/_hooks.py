#

"""Tox plugin hooks."""

import pathlib
import typing

import poetry.core.factory
import poetry.core.poetry
import tox

if typing.TYPE_CHECKING:
    IndexServersT = typing.Tuple[
        tox.config.IndexServerConfig,  # PIP_INDEX_URL
        typing.List[tox.config.IndexServerConfig],  # PIP_EXTRA_INDEX_URL
    ]

PIP_DEFAULT_INDEX_SERVER_URL = 'https://pypi.org/simple'
PIP_DEFAULT_INDEX_SERVER_NAME = 'pypi'


class _Exception(Exception):
    """Base exception."""


class NoPoetryFound(_Exception):
    """No poetry found."""


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
            "Use Poetry's source repositories. Set 'pip_env_vars' to set as "
            "Pip environment variables ('PIP_INDEX_URL', and "
            "'PIP_EXTRA_INDEX_URL')."
        ),
    )
    parser.add_testenv_attribute(
        'poetry_install_locked_dependencies',
        'bool',
        "Install locked versions of the dependencies according to lock file",
        default=False,
    )


@tox.hookimpl  # type: ignore[misc]
def tox_configure(config: tox.config.Config) -> None:
    """Set hook."""
    try:
        poetry_ = _get_poetry(config.setupdir)
    except NoPoetryFound:
        pass
    else:
        pinned_deps = _get_pinned_deps(poetry_)
        #
        dev_deps = _get_dev_requirements(poetry_)
        _add_dev_dependencies(config, dev_deps)
        #
        index_servers = _get_index_servers(poetry_)
        _add_index_servers(config, index_servers)


def _add_dev_dependencies(
        tox_config: tox.config.Config,
        dev_dep_configs: typing.Iterable[tox.config.DepConfig],
) -> None:
    #
    skip_envs = [
        tox_config.isolated_build_env,
        tox_config.provision_tox_env,
    ]
    #
    for env_config in tox_config.envconfigs.values():
        if env_config.envname not in skip_envs:
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


def _get_poetry(project_root_path: pathlib.Path) -> poetry.core.poetry.Poetry:
    poetry_factory = poetry.core.factory.Factory()
    try:
        poetry_ = poetry_factory.create_poetry(str(project_root_path))
    except RuntimeError as runtime_error:
        raise NoPoetryFound from runtime_error
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


def _get_pinned_deps(
        poetry_: poetry.core.poetry.Poetry,
) -> typing.List[tox.config.DepConfig]:
    #
    pinned_deps = [
        tox.config.DepConfig(dependency.to_dependency().to_pep_508())
        for dependency in poetry_.locker.get_packages()
    ]
    return pinned_deps


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


# EOF
