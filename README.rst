..


Introduction
============

Tox plugin to let Tox know about Poetry's development dependencies.


Repositories
------------

Distributions:

* https://pypi.org/project/tox-poetry-dev-dependencies/


Source code:

* https://github.com/sinoroc/tox-poetry-dev-dependencies
* https://gitlab.com/sinoroc/tox-poetry-dev-dependencies


Usage
=====

Installation
------------

It is a plugin for Tox and it is available on PyPI, install it however best fits the workflow. A useful thing to know though, is that starting with Tox version *3.8* it is possible to enforce the installation (in an isolated environment) of the plugin directly from within the ``tox.ini`` file, thanks to the ``requires`` setting (Tox *3.2*) and the *auto-provisioning* feature (Tox *3.8*):

.. code::

    [tox]
    requires =
        tox-poetry-dev-dependencies


* https://tox.readthedocs.io/en/latest/config.html#conf-requires
* https://tox.readthedocs.io/en/latest/example/basic.html#tox-auto-provisioning

By default the plugin does not do anything. Use one of the following settings to activate the corresponding features.


``add_poetry_dev_dependencies``
-------------------------------

Set the ``testenv`` setting ``add_poetry_dev_dependencies`` to ``True`` to let Tox install Poetry's development dependencies in the test environment.

.. code::

    [testenv:example]
    # ...
    add_poetry_dev_dependencies = True



``poetry_use_source_repos``
---------------------------

Set the ``testenv`` setting ``poetry_use_source_repos`` to ``pip_env_vars`` to let Tox set the ``PIP_EXTRA_URL`` and ``PIP_EXTRA_INDEX_URL`` environment variables accordingly.

.. code::

    [testenv:example]
    # ...
    poetry_use_source_repos = pip_env_vars


This will read sections such as the following from the ``pyproject.toml`` file:

.. code::

    [[tool.poetry.source]]
    name = "project-alpha"
    url = "https://alpha.example/simple"
    secondary = true

    [[tool.poetry.source]]
    name = "project-bravo"
    url = "https://bravo.example/simple"

    [[tool.poetry.source]]
    name = "project-charlie"
    url = "https://charlie.example/simple"
    default = true


and set the environment variables:

.. code::

    PIP_INDEX_URL=https://charlie.example/simple
    PIP_EXTRA_INDEX_URL=https://bravo.example/simple https://pypi.org/simple https://alpha.example/simple


If there is at least one non ``secondary`` source repository defined, then pip's default index server (*PyPI* ``https://pypi.org/simple``) is placed in ``PIP_EXTRA_INDEX_URL`` right before any ``secondary`` respository.

If pip's environment variables are already defined then they are not overwritten. For example in a command like the following, the plugin does not overwrite the environment variable.

.. code::

    PIP_INDEX_URL=https://delta.example/simple tox


.. EOF
