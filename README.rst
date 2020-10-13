..


.. contents::
    :backlinks: none


Introduction
============

Tox plugin to help working with Poetry-based projects.


Repositories
------------

Distributions:

* https://pypi.org/project/tox-poetry-dev-dependencies/


Source code:

* https://github.com/sinoroc/tox-poetry-dev-dependencies
* https://gitlab.com/sinoroc/tox-poetry-dev-dependencies


Usage
=====

By default the plugin does not do anything. Use one of the following settings to activate the corresponding features.


``poetry_experimental_add_locked_dependencies``
-----------------------------------------------

Set the ``testenv`` setting ``poetry_experimental_add_locked_dependencies`` to ``True`` to let Tox add Poetry's locked dependencies from the *lockfile* to the ``deps`` list in the test environment.

.. code::

    [testenv:example]
    # ...
    poetry_experimental_add_locked_dependencies = True

If ``poetry_add_dev_dependencies`` is set as well then the development dependencies are added with the version from the *lockfile*.


``poetry_add_dev_dependencies``
-------------------------------

Set the ``testenv`` setting ``poetry_add_dev_dependencies`` to ``True`` to let Tox add Poetry's development dependencies to the ``deps`` list in the test environment.

.. code::

    [testenv:example]
    # ...
    poetry_add_dev_dependencies = True


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


``poetry_experimental_no_virtual_env``
--------------------------------------

*Experimental feature*

Set the ``testenv`` setting ``poetry_experimental_no_virtual_env`` to ``True`` to skip the creation of a virtual environment for this test environment.

.. code::

    [testenv:real]
    deps =
    poetry_experimental_no_virtual_env = True
    skip_install = True


This might be useful in cases where all the required dependencies and tools are already available, i.e. they are already installed in global or user *site packages* directory, or maybe they are already installed directly in the system (via ``apt``, ``yum``, ``pacman``, etc.).

For such environments it might be best to skip the installation of the project (``skip_install``) as well as keeping the list of dependencies empty (``deps``).


Appendix
========

Installation
------------

It is a plugin for Tox and it is available on PyPI, install it however best fits the workflow. A useful thing to know though, is that starting with Tox version *3.8* it is possible to enforce the installation (in an isolated environment) of the plugin directly from within the ``tox.ini`` file, thanks to the ``requires`` setting (Tox *3.2*) and the *auto-provisioning* feature (Tox *3.8*):

.. code::

    [tox]
    requires =
        tox-poetry-dev-dependencies


* https://tox.readthedocs.io/en/latest/config.html#conf-requires
* https://tox.readthedocs.io/en/latest/example/basic.html#tox-auto-provisioning


Similar projects
----------------

* https://pypi.org/project/tox-poetry-installer/
* https://pypi.org/project/tox-poetry/


.. EOF
