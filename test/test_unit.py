#

"""Unit tests."""

import unittest

import tox_poetry_dev_dependencies


class TestProjectVersion(unittest.TestCase):
    """Project version string."""

    def test_project_has_version_string(self) -> None:
        """Project should have a vesion string."""
        self.assertIn('__version__', dir(tox_poetry_dev_dependencies))
        self.assertIsInstance(tox_poetry_dev_dependencies.__version__, str)


# EOF
