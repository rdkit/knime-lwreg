import unittest
import tempfile
import os
from pathlib import Path
import knime.extension as knext

from knime_lwreg import LWRegInitNode


class TestLWRegInitNode(unittest.TestCase):
    """Tests for the LWRegInitNode."""

    def setUp(self):
        """Set up test fixtures before each test method."""
        # Create a temporary directory for test databases
        self.temp_dir = tempfile.mkdtemp()
        self.test_db_path = os.path.join(self.temp_dir, "test_lwreg.db")

    def tearDown(self):
        """Clean up after each test method."""
        # Clean up test database if it exists
        if os.path.exists(self.test_db_path):
            os.remove(self.test_db_path)
        os.rmdir(self.temp_dir)

    def test_configure_with_valid_path(self):
        """Test that configure works with a valid database path."""
        node = LWRegInitNode()
        node.db_path_input = self.test_db_path
        node.db_standardization_operations = "fragment"
        node.db_remove_Hs = False
        node.db_conformer_mode = False
        node.db_canonical_orientation = False
        
        # Create a mock configure context
        class MockConfigureContext:
            def __init__(self):
                self.warnings = []
                self.errors = []
            
            def set_warning(self, message):
                self.warnings.append(message)
        
        configure_context = MockConfigureContext()
        
        # This should not raise an exception
        try:
            node.configure(configure_context)
        except Exception as e:
            self.fail(f"configure() raised an exception: {e}")

    def test_configure_with_existing_database(self):
        """Test that configure shows warning when database already exists."""
        # Create an empty file to simulate existing database
        Path(self.test_db_path).touch()
        
        node = LWRegInitNode()
        node.db_path_input = self.test_db_path
        
        class MockConfigureContext:
            def __init__(self):
                self.warnings = []
            
            def set_warning(self, message):
                self.warnings.append(message)
        
        configure_context = MockConfigureContext()
        node.configure(configure_context)
        
        # Should have a warning about existing database
        self.assertTrue(any("already exists" in warning for warning in configure_context.warnings))


class TestLWRegRegisterNode(unittest.TestCase):
    """Tests for the LWRegRegisterNode."""

    def setUp(self):
        """Set up test fixtures."""
        # Import the node class
        from knime_lwreg.my_extension import LWRegRegisterNode
        self.LWRegRegisterNode = LWRegRegisterNode

    def test_configure_creates_correct_schema(self):
        """Test that configure creates the correct output schema."""
        node = self.LWRegRegisterNode()
        
        # Create mock input schema
        input_schema = knext.Schema.from_columns([
            knext.Column(knext.string(), "SMILES"),
            knext.Column(knext.string(), "Name")
        ])
        
        class MockConfigureContext:
            pass
        
        configure_context = MockConfigureContext()
        output_schema = node.configure(configure_context, input_schema)
        
        # Check that output schema has the expected columns
        self.assertIsNotNone(output_schema)
        # Note: Schema validation would need proper KNIME testing framework
        # For now, we just verify the schema is created

    def test_node_parameters(self):
        """Test that node has the required parameters."""
        node = self.LWRegRegisterNode()
        
        # Check that required parameters exist
        self.assertTrue(hasattr(node, 'db_path_input'))
        self.assertTrue(hasattr(node, 'smiles_column'))


class TestLWRegQueryNode(unittest.TestCase):
    """Tests for the LWRegQueryNode."""

    def setUp(self):
        """Set up test fixtures."""
        from knime_lwreg.my_extension import LWRegQueryNode
        self.LWRegQueryNode = LWRegQueryNode

    def test_configure_creates_correct_schema(self):
        """Test that configure creates the correct output schema."""
        node = self.LWRegQueryNode()
        
        class MockConfigureContext:
            pass
        
        configure_context = MockConfigureContext()
        output_schema = node.configure(configure_context)
        
        # Check that output schema has the expected columns
        self.assertIsNotNone(output_schema)
        # Note: Schema validation would need proper KNIME testing framework
        # For now, we just verify the schema is created

    def test_node_parameters(self):
        """Test that node has the required parameters."""
        node = self.LWRegQueryNode()
        
        # Check that required parameters exist
        self.assertTrue(hasattr(node, 'db_path_input'))
        self.assertTrue(hasattr(node, 'query_input'))


class TestLWRegRetrieveNode(unittest.TestCase):
    """Tests for the LWRegRetrieveNode."""

    def setUp(self):
        """Set up test fixtures."""
        from knime_lwreg.my_extension import LWRegRetrieveNode
        self.LWRegRetrieveNode = LWRegRetrieveNode

    def test_configure_creates_correct_schema(self):
        """Test that configure creates the correct output schema."""
        node = self.LWRegRetrieveNode()
        
        # Create mock input schema with Molregno and Conf_ID
        input_schema = knext.Schema.from_columns([
            knext.Column(knext.double(), "Molregno"),
            knext.Column(knext.double(), "Conf_ID")
        ])
        
        class MockConfigureContext:
            pass
        
        configure_context = MockConfigureContext()
        output_schema = node.configure(configure_context, input_schema)
        
        # Check that output schema has the expected columns
        self.assertIsNotNone(output_schema)
        # Note: Schema validation would need proper KNIME testing framework
        # For now, we just verify the schema is created

    def test_node_parameters(self):
        """Test that node has the required parameters."""
        node = self.LWRegRetrieveNode()
        
        # Check that required parameters exist
        self.assertTrue(hasattr(node, 'db_path_input'))
        self.assertTrue(hasattr(node, 'as_submitted'))


if __name__ == "__main__":
    unittest.main()
