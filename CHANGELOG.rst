..


.. Keep the current version number on line number 6

0.0.9
=====

*2020-11-18*

* Fix issue occuring when there are no 'dev' dependencies in the 'lockfile'


0.0.8
=====

*2020-11-16*

* Fix some compatibility issues for Python 3.5


0.0.7
=====

*2020-11-09*

* Fix issue with unwarranted exceptions for unsupported locked dependencies.


0.0.6
=====

*2020-11-08*

* Add support for Python 3.9
* Fix issue with type hints that would cause failures on Python interpreters where `from __future__ import annotations` is not available (Python < 3.7).


0.0.5
=====

*2020-10-19*

* Add support for URL dependencies in lockfile


0.0.4
=====

*2020-10-13*

* Rename setting ``add_poetry_dev_dependencies`` to ``poetry_add_dev_dependencies``.
* Add the ``poetry_experimental_add_locked_dependencies`` setting to let Tox add Poetry's locked dependencies from Poetry's lockfile (experimental feature).
* Remove the *PEP 396* ``__version__``. This also allows getting rid of the dependency on `importlib-metadata``.


0.0.3
=====

*2020-10-06*

* Add the ``poetry_experimental_no_virtual_env`` setting to allow skipping the creation of the virtual environment (experimental feature)


0.0.2
=====

*2020-09-28*

* Allow download from alternative repositories (without authentication) for pip via environment variables


0.0.1
=====

*2020-09-17*

* Fix a small issue that blocked the usage under Python 3.5
* Make the dependencies mandatory


0.0.0
=====

*2020-09-11*

* Initial implementation


.. EOF
