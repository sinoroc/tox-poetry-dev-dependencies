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
