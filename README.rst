..


Introduction
============

Let Tox know about Poetry's development dependencies.


Repositories
------------

Distributions:

* https://pypi.org/project/tox-poetry-dev-dependencies/


Source code:

* https://github.com/sinoroc/tox-poetry-dev-dependencies
* https://gitlab.com/sinoroc/tox-poetry-dev-dependencies


Usage
=====

Set the ``add_poetry_dev_dependencies`` to ``True`` to let Tox install Poetry's
development dependencies in the test environment.

.. code::

    [testenv]
    add_poetry_dev_dependencies = True
    # ...


.. EOF
