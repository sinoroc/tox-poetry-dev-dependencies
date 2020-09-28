#

"""Meta information."""

try:
    import importlib.metadata as importlib_metadata
except ImportError:
    import importlib_metadata  # type: ignore[no-redef]

PROJECT_NAME = 'tox-poetry-dev-dependencies'

_DISTRIBUTION_METADATA = importlib_metadata.metadata(PROJECT_NAME)

VERSION = _DISTRIBUTION_METADATA['Version']

# EOF
