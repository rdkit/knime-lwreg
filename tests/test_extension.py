import unittest
import pandas as pd
import knime.extension as knext
import knime.extension.testing as ktest
from rdkit import Chem

from knime_lwreg import LWRegInitNode


class TestLWRegInitNode(unittest.TestCase):
    """Tests for the LWRegInitNode."""

    @classmethod
    def setUpClass(cls) -> None:
        # The test plugin and mock chemistry types are registered in tests/conftest.py
        pass

    def test_execute_adds_rdkitmol_from_smiles(self):
        """Test that the node correctly adds RDKitMol column from SMILES."""
        # Create input data frame with SMILES
        input_data = pd.DataFrame({"SMILES": ["CCO", "CCN", "CCC"]})


if __name__ == "__main__":
    unittest.main()
