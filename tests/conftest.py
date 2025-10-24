import os
import sys
import logging
from datetime import datetime

LOGGER = logging.getLogger(__name__)

# Ensure repository root is on sys.path so `import src` works to find the source code
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

# ----------------------------------------------------------------------------------------------------
# Add support for chemistry types
#
# The following code creates stubs for the chemistry types so that
# they can be easily imported in tests. e.g.:
# import knime.types.chemistry as cet

TEST_DIR = os.path.dirname(__file__)
MOCK_PY_FILE = os.path.join(
    TEST_DIR, "test", "python", "src", "org", "knime", "types", "chemistry.py"
)
MOCK_PY_WEB_SRC = "https://bitbucket.org/KNIME/knime-chemistry/src/master/org.knime.chem.types/python/src/org/knime/types/chemistry.py"  # Use GitHub if available
MOCK_PY_SRC = os.path.join(TEST_DIR, "test", "python", "src")
PLUGIN_XML = os.path.join(TEST_DIR, "test", "plugin.xml")
PLUGIN_XML_WEB_SRC = "https://bitbucket.org/KNIME/knime-chemistry/src/master/org.knime.chem.types/plugin.xml"  # Use GitHub if available

# Buffer for any update error so we can report it once pytest logging is configured
UPDATE_ERROR_MSG: str | None = None

# Try to update chemistry.py and plugin.xml from the provided address. If it fails inform the user to be responsible
try:
    import urllib.request

    # Update chemistry.py
    with urllib.request.urlopen(MOCK_PY_WEB_SRC) as response:
        with open(MOCK_PY_FILE, "wb") as out_file:
            out_file.write(response.read())
    # Update plugin.xml
    with urllib.request.urlopen(PLUGIN_XML_WEB_SRC) as response:
        with open(PLUGIN_XML, "wb") as out_file:
            out_file.write(response.read())
except Exception as e:
    # If the update fails, store message to log later when pytest logging is configured
    UPDATE_ERROR_MSG = f"{e}"

# Ensure the mock chemistry package is importable
if MOCK_PY_SRC not in sys.path:
    sys.path.insert(0, MOCK_PY_SRC)
# Register the test plugin (adds python/src to path for KNIME plugin resolution)
try:
    import knime.extension.testing as ktest

    if os.path.isfile(PLUGIN_XML):
        ktest.register_extension(PLUGIN_XML)
except Exception:
    # Keep tests importable even if KNIME test utilities are unavailable
    pass


def pytest_sessionstart(session):  # type: ignore[unused-argument]
    """Emit conftest logs after pytest has configured its logging handlers."""
    # Report update issues (if any) and current file status
    if UPDATE_ERROR_MSG:
        LOGGER.warning(
            f"Failed to update chemistry stubs: {UPDATE_ERROR_MSG}. Please update them manually."
        )

    def _fmt_mtime(path: str) -> str:
        try:
            ts = os.path.getmtime(path)
            return datetime.fromtimestamp(ts).strftime("%Y-%m-%d-%H-%M")
        except Exception:
            return "n/a"

    LOGGER.info(
        f"plugin.xml: {PLUGIN_XML} | exists: {os.path.isfile(PLUGIN_XML)} | last modified: {_fmt_mtime(PLUGIN_XML)}"
    )
    LOGGER.info(
        f"chemistry.py: {MOCK_PY_FILE} | exists: {os.path.isfile(MOCK_PY_FILE)} | last modified: {_fmt_mtime(MOCK_PY_FILE)}"
    )
