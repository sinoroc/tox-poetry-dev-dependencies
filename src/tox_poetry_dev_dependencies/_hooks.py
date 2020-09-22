#

"""Tox plugin hooks."""

import pathlib
import typing

import poetry.core.factory
import tox


class _Exception(Exception):
    """Base exception."""


class NoPoetryFound(_Exception):
    """No poetry found."""


@tox.hookimpl  # type: ignore[misc]
def tox_addoption(parser: tox.config.Parser) -> None:
    """Set hook."""
    parser.add_testenv_attribute(
        'add_poetry_dev_dependencies',
        'bool',
        "Add Poetry's 'dev-dependencies' to the test environment.",
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
        dev_deps = _get_dev_requirements(poetry_)
        _add_dev_dependencies(config, dev_deps)


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


# EOF
