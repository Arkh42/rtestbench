"""Test for the rtestbench module."""


import pytest

import rtestbench


@pytest.fixture
def sim_visa_rm():
    """Returns a simulated VISA resource manager."""

    import visa

    return visa.ResourceManager('@sim')

@pytest.fixture
def rtb_quiet():
    """Returns a non-verbose RTestBench."""

    import logging
    from rtestbench.core import RTestBench

    rtb = RTestBench(verbose=False)
    logging.disable(logging.CRITICAL)

    return rtb


def test_initialize(rtb_quiet):
    assert hasattr(rtb_quiet, "_VERBOSE")
    assert hasattr(rtb_quiet, "_attached_resources")
    assert hasattr(rtb_quiet, "chat")
    assert hasattr(rtb_quiet, "logger")

def test_detect_resources(rtb_quiet):
    detected_resources = rtb_quiet.detect_resources()
    assert isinstance(detected_resources, tuple)

def test_attach_resource(sim_visa_rm, rtb_quiet):
    with pytest.raises(ValueError):
        rtb_quiet.attach_resource('ASRL1::INSTR')
