..


Git commit messages
===================

As this project is hosted on multiple platforms (GitHub and GitLab currently), every line of the git commit messages mentioning a magic number (such as issue or pull request number for example) should be prefixed with the name of the platform. For example a line in a commit message of the form:

.. code::

    Closes #XX


should be instead written as:

.. code::

    GitHub: closes #XX
    GitLab: refs #ZZ
    GitLab: refs #YY
    SomeThing: whatever #XX


Some tools (Gerrit for example) can be configured (with regexes for example) to correctly link to the items on the right platform.

* https://gerrit-review.googlesource.com/Documentation/config-gerrit.html#commentlink


Hacking
=======

This project makes extensive use of `tox`_, `pytest`_, and `GNU Make`_.


Development environment
-----------------------

Use following command to create a Python virtual environment with all necessary dependencies::

    tox --recreate -e develop

This creates a Python virtual environment in the ``.tox/develop`` directory. It can be activated with the following command::

    . .tox/develop/bin/activate


Run test suite
--------------

In a Python virtual environment run the following command::

    make review

Outside of a Python virtual environment run the following command::

    tox --recreate


Build and package
-----------------

In a Python virtual environment run the following command::

    make package

Outside of a Python virtual environment run the following command::

    tox --recreate -e package


.. Links

.. _`GNU Make`: https://www.gnu.org/software/make/
.. _`pytest`: https://pytest.org/
.. _`tox`: https://tox.readthedocs.io/


.. EOF
