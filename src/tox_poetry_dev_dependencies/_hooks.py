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
        requirements = _get_dev_requirements(config.setupdir)
    except NoPoetryFound:
        pass
    else:
        skip_envs = [
            config.isolated_build_env,
            config.provision_tox_env,
        ]
        for envconfig in config.envconfigs.values():
            if envconfig.envname not in skip_envs:
                if envconfig.add_poetry_dev_dependencies is True:
                    for requirement in requirements:
                        dep_config = tox.config.DepConfig(requirement)
                        envconfig.deps.append(dep_config)


def _get_dev_requirements(project_root_path: pathlib.Path) -> typing.List[str]:
    poetry_factory = poetry.core.factory.Factory()
    try:
        poetry_ = poetry_factory.create_poetry(project_root_path)
    except RuntimeError as runtime_error:
        raise NoPoetryFound from runtime_error
    else:
        requirements = [
            dependency.to_pep_508()
            for dependency
            in poetry_.package.dev_requires
        ]
    return requirements


# EOF
