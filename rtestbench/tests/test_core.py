"""Test for the core module."""


import pytest

import numpy as np

import rtestbench


##########################
# Generic tool interface #
##########################

@pytest.fixture
def toolInfo_empty():
    """Returns an empty ToolInfo object, i.e., with all fields equal to None."""

    from rtestbench.core import ToolInfo
    return ToolInfo()

@pytest.fixture
def toolProperties_empty():
    """Returns an empty ToolProperties object, i.e., with default values."""

    from rtestbench.core import ToolProperties
    return ToolProperties()

# --------

def test_toolInfo_attributes(toolInfo_empty):
    assert hasattr(toolInfo_empty, "family")
    assert hasattr(toolInfo_empty, "manufacturer")
    assert hasattr(toolInfo_empty, "model")
    assert hasattr(toolInfo_empty, "serial_number")

def test_toolInfo_init(toolInfo_empty):
    assert toolInfo_empty.family is None
    assert toolInfo_empty.manufacturer is None
    assert toolInfo_empty.model is None
    assert toolInfo_empty.serial_number is None

# --------

def test_toolProperties_attributes(toolProperties_empty):
    assert hasattr(toolProperties_empty, "data_container")
    assert hasattr(toolProperties_empty, "transfer_formats")
    assert hasattr(toolProperties_empty, "bin_data_header")
    assert hasattr(toolProperties_empty, "endian")

def test_toolProperties_init(toolProperties_empty):
    assert toolProperties_empty.data_container is np.ndarray
    assert toolProperties_empty.transfer_formats == []
    assert toolProperties_empty.bin_data_header is None
    assert toolProperties_empty.endian is None

def test_toolProperties_datacontainer(toolProperties_empty):
    # Permitted values
    toolProperties_empty.data_container = list
    assert toolProperties_empty.data_container is list
    toolProperties_empty.data_container = tuple
    assert toolProperties_empty.data_container is tuple
    toolProperties_empty.data_container = np.ndarray
    assert toolProperties_empty.data_container is np.ndarray

    # Forbidden values
    with pytest.raises(ValueError):
        toolProperties_empty.data_container = float
        toolProperties_empty.data_container = str

def test_toolProperties_transferformats(toolProperties_empty):
    # Permitted values
    toolProperties_empty.transfer_formats = ['text']
    assert toolProperties_empty.transfer_formats == ['text']
    toolProperties_empty.transfer_formats = ['ascii']
    assert toolProperties_empty.transfer_formats == ['ascii']
    toolProperties_empty.transfer_formats = ['bin']
    assert toolProperties_empty.transfer_formats == ['bin']
    toolProperties_empty.transfer_formats = ['bin32']
    assert toolProperties_empty.transfer_formats == ['bin32']
    toolProperties_empty.transfer_formats = ['bin64']
    assert toolProperties_empty.transfer_formats == ['bin64']

    # Combination of permitted values
    toolProperties_empty.transfer_formats = ['text', 'bin']
    assert toolProperties_empty.transfer_formats == ['text', 'bin']
    toolProperties_empty.transfer_formats = ['ascii', 'bin32', 'bin64']
    assert toolProperties_empty.transfer_formats == ['ascii', 'bin32', 'bin64']

    # Forbidden values
    with pytest.raises(ValueError):
        toolProperties_empty.transfer_formats = ['toto']
        toolProperties_empty.transfer_formats = ['toto', 'text']
        toolProperties_empty.transfer_formats = ['text', 'toto']

def test_toolProperties_endian(toolProperties_empty):
    # Permitted values
    toolProperties_empty.endian = 'big'
    assert toolProperties_empty.endian == 'big'
    toolProperties_empty.endian = 'little'
    assert toolProperties_empty.endian == 'little'

    # Forbidden values
    with pytest.raises(ValueError):
        toolProperties_empty.endian = 'toto'



#######################
# R-testbench manager #
#######################

@pytest.fixture
def sim_visa_rm():
    """Returns a simulated VISA resource manager."""

    import visa

    return visa.ResourceManager('@sim')

@pytest.fixture
def rtb_quiet():
    """Returns a non-verbose RTestBench."""

    import logging
    from rtestbench.core import RTestBenchManager

    rtb = RTestBenchManager(verbose=False)
    logging.disable(logging.CRITICAL)

    return rtb


# Constructor

def test_initialize(rtb_quiet):
    assert hasattr(rtb_quiet, "_VERBOSE")
    assert hasattr(rtb_quiet, "_attached_resources")
    assert hasattr(rtb_quiet, "chat")
    assert hasattr(rtb_quiet, "logger")


# Destructor and related close functions

def test_close_visa_rm(rtb_quiet):
    assert rtb_quiet._visa_rm is not None
    rtb_quiet._close_visa_rm()
    assert rtb_quiet._visa_rm is None


# Information about resources

def test_detect_resources(sim_visa_rm, rtb_quiet):
    detected_resources = rtb_quiet.detect_resources()
    assert detected_resources
    assert isinstance(detected_resources, tuple)


# Resource management

def test_attach_resource(sim_visa_rm, rtb_quiet):
    with pytest.raises(ValueError):
        rtb_quiet.attach_resource('ASRL1::INSTR')
