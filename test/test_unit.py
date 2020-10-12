#

"""Unit tests."""

import types
import unittest

import tox_poetry_dev_dependencies


class TestDummy(unittest.TestCase):
    """Dummy."""

    def test_dummy(self) -> None:
        """Dummy test."""
        self.assertIsInstance(tox_poetry_dev_dependencies, types.ModuleType)


# EOF
