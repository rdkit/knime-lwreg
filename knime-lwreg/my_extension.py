import logging
from pathlib import Path

import knime.extension as knext
import lwreg
import lwreg.standardization_lib
import numpy as np
import pandas as pd
from lwreg import utils

LOGGER = logging.getLogger(__name__)

# Importing LWReg: https://github.com/rinikerlab/lightweight-registration/

lwreg.set_default_config(utils.defaultConfig())  # Configure LWReg with default settings

# Specifying our category: https://docs.knime.com/latest/pure_python_node_extensions_guide/index.html#_specifying_the_node_category
# lwreg_category = knext.category(
#     path="/community",
#     level_id="lwreg_integration",
#     name="LWReg Integration",
#     description="LWReg KNIME Integration",
#     icon="icon.png",
# )


#################################
### LWReg Initialize Database ###
#################################
@knext.node(
    name="LWReg Initialize Database",
    node_type=knext.NodeType.SOURCE,
    icon_path="icon.png",
    category="/",
)
class LWRegInitNode:
    """Initialize new database
        This node can be used to initialize a LWReg database. In case the database already exists, nothing happens.
        Which Standardization should be applied?

    | Option | Description |
    | ------- | ----------- |
    | none | does not modify the molecule |
    | sanitize | Standard RDKit standardization |
    | fragment | Fragment parent of molecule |
    | charge | Charge Parent of molecule |
    | tautomer | Tautomer parent of molecule |

    """
  
    db_path_input = knext.StringParameter(
        label="Database Path",
        description="Specify the full path to the LWREG database file.",
        default_value="lwreg.sql",
    )
    db_standardization_operations = knext.StringParameter(
        label="Standardization Operation",
        enum=["none", "sanitize", "fragment", "charge", "tautomer"],
        default_value="fragment",
        description="Which Standardization should be applied?",
    )
    db_remove_Hs = knext.BoolParameter(
        "Remove Hydrogens", description="Should Hydrogens be removed?"
    )
    db_conformer_mode = knext.BoolParameter(
        "Conformer Mode", description="Should Conformers be registered?"
    )
    db_canonical_orientation = knext.BoolParameter(
        "Canonical Orientation", description="Should the orientation be canonicalized?"
    )

    def configure(self, configure_context):
        db_path = Path(self.db_path_input)

        if db_path.exists():
            configure_context.set_warning(
                "The selected database file already exists. Nothing to do."
            )

        if not self.db_path_input or self.db_path_input.strip() == "":
            configure_context.set_warning(
                "A valid path to the database must be provided."
            )
            raise ValueError("You must provide a valid path to the database.")

        if not db_path.parent.exists():
            configure_context.set_warning(f"Directory {db_path.parent} does not exist.")
            raise ValueError("You must provide a valid path to the database.")

    def execute(self, exec_context):
        """Executes LWREG database initialization if checkbox is checked."""
        if Path(self.db_path_input).exists():
            exec_context.set_progress(
                1.0, "LWREG Database already exists. Nothing to do."
            )
            return

        standardization = [self.db_standardization_operations]
        if self.db_canonical_orientation:
            standardization.append("canonicalize")

        init_custom_config = {
            "dbname": self.db_path_input,
            "dbtype": "sqlite3",
            "standardization": standardization,
            "removeHs": 1 if self.db_remove_Hs else 0,
            "useTautomerHashv2": 0,
            "registerConformers": 1 if self.db_conformer_mode else 0,
            "numConformerDigits": 3,
            "lwregSchema": "",  # Only relevant for PostgreSQL
        }

        exec_context.flow_variables["lwreg_db_path"] = self.db_path_input
        exec_context.set_progress(0.0, "Initializing LWREG Database...")
        utils._initdb(config=init_custom_config, confirm=True)
        exec_context.set_progress(1.0, "LWREG Database initialized successfully.")


################################
### LWReg Register Compounds ###
################################
@knext.node(
    name="LWReg Register Compounds",
    node_type=knext.NodeType.MANIPULATOR,
    icon_path="icon.png",
    category="/",
)
@knext.input_table(
    name="Input Compounds", description="Input table containing compounds to register."
)
@knext.output_table(
    name="Registration Results",
    description="Outputs registration results with compound IDs.",
)
class LWRegRegisterNode:
    """Registers compounds to LWReg database.
    This node takes an input table of compounds (e.g., SMILES strings) and registers them into the LWReg database.
    """

    # String input to specify the database path
    db_path_input = knext.StringParameter(
        label="Database Path",
        description="Specify the path to the LWREG database file.",
        default_value="C:/path/to/your/lwreg_database.sqlt",
    )

    # String input to specify the column containing SMILES strings
    smiles_column = knext.ColumnParameter(
        label="SMILES Column",
        description="Select the column containing SMILES strings for registration.",
        port_index=0,  # Refers to the first input port (input table)
    )

    def configure(self, configure_context, input_schema):
        output_schema = knext.Schema.from_columns(
            [
                knext.Column(
                    knext.string(), "SMILES"
                ),  # SMILES column will be a string
                knext.Column(
                    knext.double(), "Compound ID"
                ),  # Compound ID will also be a string
                knext.Column(knext.string(), "Status"),  # Status will be a string
            ]
        )
        return output_schema

    def execute(self, exec_context, input_table):
        exec_context.set_progress(0.0, "Registering compounds...")

        # Set the database path configuration for lwreg
        lwreg.set_default_config({"dbname": self.db_path_input, "dbtype": "sqlite3"})

        # Convert input_table to pandas DataFrame for easier processing
        input_df = input_table.to_pandas()

        # Extract SMILES column
        if self.smiles_column not in input_df.columns:
            raise ValueError(
                f"Column '{self.smiles_column}' not found in the input data."
            )
        smiles_data = input_df[self.smiles_column]

        # Create a list to store the registration results
        registration_results = []

        # Register each compound in the LWReg database
        for idx, smiles in smiles_data.items():
            try:
                # Call the correct `register` function from lwreg.utils
                compound_id = lwreg.register(smiles=smiles)

                # Check if the compound_id is a failure reason, i.e., an instance of RegistrationFailureReasons
                if isinstance(compound_id, lwreg.RegistrationFailureReasons):
                    status = f"Failed: {compound_id.name}"  # Get the name of the failure reason (e.g., PARSE_FAILURE)
                    registration_results.append(
                        {
                            "SMILES": smiles,
                            "Compound ID": np.nan,  # np.nan does not throw KNIME off regarding data types, as None would.
                            "Status": status,
                        }
                    )
                else:
                    status = "Success"
                    registration_results.append(
                        {"SMILES": smiles, "Compound ID": compound_id, "Status": status}
                    )

            except Exception as e:
                LOGGER.error(f"Failed to register compound '{smiles}': {e}")

                # Handle unexpected exceptions
                registration_results.append(
                    {"SMILES": smiles, "Compound ID": np.nan, "Status": f"Failed: {e}"}
                )

        # Create a pandas DataFrame with the registration results
        results_df = pd.DataFrame(registration_results)

        # Return the results as a KNIME table
        return knext.Table.from_pandas(results_df)


########################
### LWReg Query Node ###
########################
@knext.node(
    name="LWReg Query",
    node_type=knext.NodeType.MANIPULATOR,
    icon_path="icon.png",
    category="/",
)
@knext.output_table(
    name="Query Results",
    description="Outputs the results of a querey to the LWReg database.",
)
class LWRegQueryNode:
    """Query the LWReg database.
    This node takes input parameters (e.g., SMILES) and queries the LWReg database.
    """

    # String input to specify the database path
    db_path_input = knext.StringParameter(
        label="Database Path",
        description="Specify the path to the LWREG database file.",
        default_value="C:/path/to/your/lwreg_database.sqlt",
    )

    # String input for the query string (e.g., SMILES or substructure)
    query_input = knext.StringParameter(
        label="Query",
        description="Specify the query to search the LWReg database (e.g., a SMILES string).",
        default_value="",
    )

    def configure(self, configure_context):
        # Define the output schema with Query, Molregno, and Conf_ID (even if Conf_ID might not be present)
        output_schema = knext.Schema.from_columns(
            [
                knext.Column(knext.string(), "Query"),  # Query will be a string
                knext.Column(knext.double(), "Molregno"),  # Molregno will be a double
                knext.Column(
                    knext.double(), "Conf_ID"
                ),  # Conf_ID will also be a double, optional but always present in schema
            ]
        )
        return output_schema

    def execute(self, exec_context):
        exec_context.set_progress(0.0, "Querying the LWReg database...")

        # Set the database path configuration for lwreg
        lwreg.set_default_config({"dbname": self.db_path_input, "dbtype": "sqlite3"})

        try:
            # Call the query function with the user-specified query input
            query_results = lwreg.query(smiles=self.query_input)

            # Check if the result contains tuples (i.e., molregno and conf_id)
            if query_results and isinstance(query_results[0], tuple):
                # Results are tuples, so we have Molregno and Conf_ID
                results_df = pd.DataFrame(
                    query_results, columns=["Molregno", "Conf_ID"]
                )
                # Convert Molregno and Conf_ID to float (double)
                results_df["Molregno"] = results_df["Molregno"].astype(float)
                results_df["Conf_ID"] = results_df["Conf_ID"].astype(float)
            else:
                # Results are single values (Molregno only), add NaN for Conf_ID
                results_df = pd.DataFrame(query_results, columns=["Molregno"])
                # Convert Molregno to float (double)
                results_df["Molregno"] = results_df["Molregno"].astype(float)
                # Add Conf_ID as NaN since it's not available
                results_df["Conf_ID"] = np.nan

            # Add the "Query" column first
            results_df.insert(
                0, "Query", self.query_input
            )  # Insert the query input as the first column

            exec_context.set_progress(1.0, "Query completed successfully.")

            # Return the results as a KNIME table
            return knext.Table.from_pandas(results_df)

        except Exception as e:
            LOGGER.error(f"Query failed: {e}")
            raise ValueError(f"Failed to query the LWReg database: {e}")


###########################
### LWReg Retrieve Node ###
###########################
@knext.node(
    name="LWReg Retrieve",
    node_type=knext.NodeType.MANIPULATOR,
    icon_path="icon.png",
    category="/",
)
@knext.input_table(
    name="Input Registry IDs",
    description="Input table containing molregnos (and optional conf_ids) to retrieve.",
)
@knext.output_table(
    name="Retrieved Molecules",
    description="Outputs the retrieved molecules with their molregno and conf_id (if applicable).",
)
class LWRegRetrieveNode:
    """Retrieve from the LWReg database.
    Retrieve molecules from the LWReg database using registry IDs as input.
    """

    # Database path
    db_path_input = knext.StringParameter(
        label="Database Path",
        description="Specify the path to the LWREG database file.",
        default_value="C:/path/to/your/lwreg_database.sqlt",
    )

    # Optionally choose to retrieve data as submitted
    as_submitted = knext.BoolParameter(
        label="Retrieve as submitted",
        description="If checked, retrieves the structure as originally submitted.",
        default_value=False,
    )

    def configure(self, configure_context, input_schema):
        # Define the output schema
        output_schema = knext.Schema.from_columns(
            [
                knext.Column(knext.double(), "Molregno"),  # Molregno will be a double
                knext.Column(
                    knext.double(), "Conf_ID"
                ),  # Conf_ID will be a double, optional but always present in schema
                knext.Column(
                    knext.string(), "Molecule Data"
                ),  # Molecule Data will be a string
            ]
        )
        return output_schema

    def execute(self, exec_context, input_table):
        exec_context.set_progress(0.0, "Retrieving molecules from LWReg...")

        # Set up the database connection using the provided path
        lwreg.set_default_config({"dbname": self.db_path_input, "dbtype": "sqlite3"})

        # Convert input_table to pandas DataFrame
        input_df = input_table.to_pandas()

        # Prepare the IDs for retrieval
        ids = []
        if "Conf_ID" in input_df.columns:
            # Extract Molregno and Conf_ID from DataFrame, flattening tuples
            ids = [
                (
                    (int(row["Molregno"]), int(row["Conf_ID"]))
                    if not pd.isna(row["Conf_ID"])
                    else int(row["Molregno"])
                )
                for index, row in input_df.iterrows()
            ]
        else:
            # Only Molregno is provided
            ids = input_df["Molregno"].astype(int).tolist()

        # Call lwreg.retrieve with the list of IDs
        try:
            retrieval_results = lwreg.retrieve(
                config=None, ids=ids, as_submitted=self.as_submitted
            )

            # Process retrieval results into a DataFrame
            results = []
            for key, (data, fmt) in retrieval_results.items():
                if isinstance(key, tuple):
                    molregno, conf_id = key
                else:
                    molregno = key
                    conf_id = np.nan  # If Conf_ID is not available

                results.append(
                    {"Molregno": molregno, "Conf_ID": conf_id, "Molecule Data": data}
                )

            # Convert results to a DataFrame
            results_df = pd.DataFrame(results)

            exec_context.set_progress(1.0, "Molecule retrieval completed.")

            # Return the results as a KNIME table
            return knext.Table.from_pandas(results_df)

        except Exception as e:
            LOGGER.error(f"Retrieval failed: {e}")
            raise ValueError(f"Failed to retrieve molecules: {e}")
