# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------
#  Copyright by KNIME AG, Zurich, Switzerland
#  Website: http://www.knime.com; Email: contact@knime.com
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License, Version 3, as
#  published by the Free Software Foundation.
#
#  This program is distributed in the hope that it will be useful, but
#  WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, see <http://www.gnu.org/licenses>.
#
#  Additional permission under GNU GPL version 3 section 7:
#
#  KNIME interoperates with ECLIPSE solely via ECLIPSE's plug-in APIs.
#  Hence, KNIME and ECLIPSE are both independent programs and are not
#  derived from each other. Should, however, the interpretation of the
#  GNU GPL Version 3 ("License") under any applicable laws result in
#  KNIME and ECLIPSE being a combined program, KNIME AG herewith grants
#  you the additional permission to use and propagate KNIME together with
#  ECLIPSE with only the license terms in place for ECLIPSE applying to
#  ECLIPSE and the GNU GPL Version 3 applying for KNIME, provided the
#  license terms of ECLIPSE themselves allow for the respective use and
#  propagation of ECLIPSE together with KNIME.
#
#  Additional permission relating to nodes for KNIME that extend the Node
#  Extension (and in particular that are based on subclasses of NodeModel,
#  NodeDialog, and NodeView) and that only interoperate with KNIME through
#  standard APIs ("Nodes"):
#  Nodes are deemed to be separate and independent programs and to not be
#  covered works.  Notwithstanding anything to the contrary in the
#  License, the License does not apply to Nodes, you are not required to
#  license Nodes under the License, and you are granted a license to
#  prepare and propagate Nodes, in each case even if such Nodes are
#  propagated with or for interoperation with KNIME.  The owner of a Node
#  may freely choose the license terms applicable to such Node, including
#  when such Node is propagated with or for interoperation with KNIME.
# ------------------------------------------------------------------------

"""
Defining Python data types to their counterparts on the Java side of the KNIME Analytics Platform.
The implemented data types in this chemistry package are:
* CDXML
* CML
* Ctab
* HELM
* Inchi
* Mol
* Mol2
* Rxn
* Sdf
* Sln
* Smarts
* Smiles

@author Steffen Fissler, KNIME GmbH, Konstanz, Germany
@author Marc Lehner, KNIME GmbH, Zurich, Switzerland
"""

import knime.api.types as kt


class AdapterValue(str):
    def __new__(cls, value, adapters=None):
        obj = str.__new__(cls, value)
        obj._adapters = adapters
        return obj


class StringBasedValueFactory(kt.PythonValueFactory):
    def __init__(self, value_class):
        self.value_class = value_class
        kt.PythonValueFactory.__init__(self, self.value_class)

    def decode(self, storage):
        if storage is None:
            return None
        return self.value_class(storage)

    def encode(self, value):
        if value is None:
            return None
        return str(value)


class AdapterValueFactory(kt.PythonValueFactory):
    def __init__(self, value_class):
        self.value_class = value_class
        kt.PythonValueFactory.__init__(self, self.value_class)

    def decode(self, storage):
        if storage is None:
            return None
        return self.value_class(storage["0"], storage["1"])

    def encode(self, value):
        if value is None:
            return None
        return {"0": str(value), "1": value._adapters}


class CDXMLValue(str):
    pass


class CDXMLValueFactory(StringBasedValueFactory):
    def __init__(self):
        super().__init__(CDXMLValue)


class CMLAdapterValue(AdapterValue):
    pass


class CMLAdapterValueFactory(AdapterValueFactory):
    def __init__(self):
        super().__init__(CMLAdapterValue)


class CMLValue(str):
    pass


class CMLValueFactory(StringBasedValueFactory):
    def __init__(self):
        super().__init__(CMLValue)


class CtabValue(str):
    pass


class CtabValueFactory(StringBasedValueFactory):
    def __init__(self):
        super().__init__(CtabValue)


class HELMAdapterValue(AdapterValue):
    pass


class HELMAdapterValueFactory(AdapterValueFactory):
    def __init__(self):
        super().__init__(HELMAdapterValue)


class HELMValue(str):
    pass


class HELMValueFactory(StringBasedValueFactory):
    def __init__(self):
        super().__init__(HELMValue)


class InchiAdapterValue(AdapterValue):
    pass


class InchiAdapterValueFactory(AdapterValueFactory):
    def __init__(self):
        super().__init__(InchiAdapterValue)


class InchiValue(str):
    pass


class InchiValueFactory(StringBasedValueFactory):
    def __init__(self):
        super().__init__(InchiValue)


class MolAdapterValue(AdapterValue):
    pass


class MolAdapterValueFactory(AdapterValueFactory):
    def __init__(self):
        super().__init__(MolAdapterValue)


class MolValue(str):
    pass


class MolValueFactory(StringBasedValueFactory):
    def __init__(self):
        super().__init__(MolValue)


class Mol2AdapterValue(AdapterValue):
    pass


class Mol2AdapterValueFactory(AdapterValueFactory):
    def __init__(self):
        super().__init__(Mol2AdapterValue)


class Mol2Value(str):
    pass


class Mol2ValueFactory(StringBasedValueFactory):
    def __init__(self):
        super().__init__(Mol2Value)


class RxnAdapterValue(AdapterValue):
    pass


class RxnAdapterValueFactory(AdapterValueFactory):
    def __init__(self):
        super().__init__(RxnAdapterValue)


class RxnValue(str):
    pass


class RxnValueFactory(StringBasedValueFactory):
    def __init__(self):
        super().__init__(RxnValue)


class SdfAdapterValue(AdapterValue):
    pass


class SdfAdapterValueFactory(AdapterValueFactory):
    def __init__(self):
        super().__init__(SdfAdapterValue)


class SdfValue(str):
    pass


class SdfValueFactory(StringBasedValueFactory):
    def __init__(self):
        super().__init__(SdfValue)


class SlnValue(str):
    pass


class SlnValueFactory(StringBasedValueFactory):
    def __init__(self):
        super().__init__(SlnValue)


class SmartsAdapterValue(AdapterValue):
    pass


class SmartsAdapterValueFactory(AdapterValueFactory):
    def __init__(self):
        super().__init__(SmartsAdapterValue)


class SmartsValue(str):
    pass


class SmartsValueFactory(StringBasedValueFactory):
    def __init__(self):
        super().__init__(SmartsValue)


class SmilesAdapterValue(AdapterValue):
    pass


class SmilesAdapterValueFactory(AdapterValueFactory):
    def __init__(self):
        super().__init__(SmilesAdapterValue)


class SmilesValue(str):
    pass


class SmilesValueFactory(StringBasedValueFactory):
    def __init__(self):
        super().__init__(SmilesValue)


###########################################################################
# RDKit adapter
# This adapter provides a way to convert KNIME chemistry types to RDKit Mol objects for use in Python.
# It includes a function to convert a pandas Series of KNIME chemistry types to a Series of
# RDKit Mol objects, and a custom accessor for pandas Series to facilitate this conversion.
# It also defines a function to check if a column contains any supported chemistry type.
###########################################################################

import functools


@functools.lru_cache(maxsize=1)
def get_knime_to_rdkit_mol():
    """Build and cache the mapping from KNIME chemistry types to RDKit converter functions."""
    try:
        from rdkit import Chem
    except ImportError:
        raise ImportError(
            "RDKit is not installed. Please install it to use chemistry types in python."
        )

    mapping = {
        # CMLAdapterValue:       Not supported 2025-07-17,
        # CMLValue:             Not supported 2025-07-17,
        CtabValue: Chem.MolFromMolBlock,
        HELMAdapterValue: Chem.MolFromHELM,
        HELMValue: Chem.MolFromHELM,
        InchiAdapterValue: Chem.MolFromInchi,
        InchiValue: Chem.MolFromInchi,
        MolAdapterValue: Chem.MolFromMolBlock,
        MolValue: Chem.MolFromMolBlock,
        Mol2AdapterValue: Chem.MolFromMol2Block,
        Mol2Value: Chem.MolFromMol2Block,
        # RxnAdapterValue:      Not supported 2025-07-17. Can contain molecules, but intended for reactions.
        # RxnValue:             Not supported 2025-07-17. Can contain molecules, but intended for reactions.
        SdfAdapterValue: Chem.MolFromMolBlock,
        SdfValue: Chem.MolFromMolBlock,
        SmartsAdapterValue: Chem.MolFromSmarts,
        SmartsValue: Chem.MolFromSmarts,
        SmilesAdapterValue: Chem.MolFromSmiles,
        SmilesValue: Chem.MolFromSmiles,
        Chem.Mol: lambda x, **kwargs: x,  # RDKit Mol passthrough; accept/ignore kwargs
    }
    # Add SLN support if available -> is not part of the rdkit build on Mac
    try:
        from rdkit.Chem import rdSLNParse

        mapping[SlnValue] = rdSLNParse.MolFromSLN
    except ImportError:
        import logging

        logging.warning(
            "Could not import SLN parser from RDKit, support for SLN missing"
        )

    return mapping


@functools.lru_cache(maxsize=1)
def get_molecule_ktypes():
    """Build and cache the set of KNIME logical types for supported molecule values."""
    import knime.extension as knext

    mapping = get_knime_to_rdkit_mol()
    return set(knext.logical(cls) for cls in mapping.keys())


def is_molecule(col: "knext.Column") -> bool:
    """True if the column holds any supported chemistry value. Example: SDF, Inchi, Smiles, etc."""
    return col.ktype in get_molecule_ktypes()


def _to_rdkit_scalar(val, **kwargs) -> "Chem.Mol":
    """Convert a KNIME chemistry type to an RDKit Mol object.
    Args:
        val: A KNIME chemistry type value (e.g., SDF, Inchi, Smiles, etc.) or an RDKit Mol.
        **kwargs: Additional keyword arguments to pass to the RDKit conversion functions.
    Returns:
        Chem.Mol: An RDKit Mol object.
    Raises:
        TypeError: If the value is not a supported chemistry type.
    """
    if val is None:
        return None
    fn = get_knime_to_rdkit_mol().get(type(val))
    if fn is not None:
        # Only coerce to str for string-based KNIME values; pass RDKit Mol through unchanged
        arg = str(val) if isinstance(val, str) else val
        return fn(arg, **kwargs)
    raise TypeError(f"Unsupported molecule value {val!r} of type {type(val)}")


def to_rdkit_series(s: "pd.Series", **kwargs) -> "pd.Series":
    """Convert a pandas Series of KNIME chemistry types to a Series of RDKit Mol objects.

    Example usage inside a KNIME Python node:
        # other node code ....
        # Select a column containing KNIME chemistry types
        molecule_column = knext.ColumnParameter(column_filter=is_molecule)

        def execute(self, exec_context, input):
            # Convert the input table to a pandas DataFrame
            input_pandas = input.to_pandas()
            # Convert the selected column to RDKitMol
            input_pandas['RDKitMol'] = to_rdkit_series(input_pandas[self.molecule_column])
            # Do something with the RDKitMol column
            # ...
            return knext.Table.from_pandas(input_pandas)

    Args:
        s (pd.Series): A pandas Series containing KNIME chemistry types.
    Returns:
        pd.Series: A pandas Series containing RDKit Mol objects.
    """
    return s.map(lambda x: _to_rdkit_scalar(x, **kwargs))


def to_rdkit_iter(s: "pd.Series", **kwargs) -> "Iterator[Chem.Mol]":
    """Yield RDKit Mol objects converted from a pandas Series of KNIME chemistry types.
    This function is a generator that yields RDKit Mol objects one by one.

    Args:
        s (pd.Series): A pandas Series containing KNIME chemistry types.

    """
    for x in s:
        yield _to_rdkit_scalar(x, **kwargs)
