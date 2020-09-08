#

"""Meta information."""

import importlib_metadata

PROJECT_NAME = 'tox-poetry-dev-dependencies'

_DISTRIBUTION_METADATA = importlib_metadata.metadata(PROJECT_NAME)

VERSION = _DISTRIBUTION_METADATA['Version']

# EOF
