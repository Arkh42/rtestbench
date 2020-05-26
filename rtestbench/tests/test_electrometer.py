"""Test for the electrometer module."""


import pytest

from rtestbench.core import ToolInfo
from rtestbench.tools.electrometer import Electrometer


@pytest.fixture
def fakeElectrometerWithoutInterface():
    info = ToolInfo()
    info.manufacturer = "Toto Tester"
    info.model = "No interface"
    info.serial_number = "42"
    info.software_version = "3.x"

    return Electrometer(info)


def test_electrometer_init(fakeElectrometerWithoutInterface):
    assert hasattr(fakeElectrometerWithoutInterface, "_info")
    assert hasattr(fakeElectrometerWithoutInterface, "_properties")
    assert hasattr(fakeElectrometerWithoutInterface, "_virtual_interface")

    assert fakeElectrometerWithoutInterface._info.family == "electrometer"

def test_electrometer_interface(fakeElectrometerWithoutInterface):
    # Scale and offset interface
    with pytest.raises(NotImplementedError):
        fakeElectrometerWithoutInterface.set_scale(axis=1, scale=10)
    with pytest.raises(NotImplementedError):
        fakeElectrometerWithoutInterface.set_offset(axis=1, offset=42)
    with pytest.raises(NotImplementedError):
        fakeElectrometerWithoutInterface.set_xscale(scale=10)
    with pytest.raises(NotImplementedError):
        fakeElectrometerWithoutInterface.set_yscale(scale=10)
    with pytest.raises(NotImplementedError):
        fakeElectrometerWithoutInterface.set_xoffset(offset=42)
    with pytest.raises(NotImplementedError):
        fakeElectrometerWithoutInterface.set_yoffset(offset=42)
    # Range interface
    with pytest.raises(NotImplementedError):
        fakeElectrometerWithoutInterface.set_range(value=42)
    with pytest.raises(NotImplementedError):
        fakeElectrometerWithoutInterface.get_range()
    with pytest.raises(NotImplementedError):
        fakeElectrometerWithoutInterface.set_autorange(switch=True)
    with pytest.raises(NotImplementedError):
        fakeElectrometerWithoutInterface.set_range_min()
    with pytest.raises(NotImplementedError):
        fakeElectrometerWithoutInterface.set_range_max()
    # Aperture (integration) time interface
    with pytest.raises(NotImplementedError):
        fakeElectrometerWithoutInterface.set_aperture_time(value=42)
    with pytest.raises(NotImplementedError):
        fakeElectrometerWithoutInterface.get_aperture_time()
    with pytest.raises(NotImplementedError):
        fakeElectrometerWithoutInterface.set_integration_time(value=42)
    with pytest.raises(NotImplementedError):
        fakeElectrometerWithoutInterface.get_integration_time()
    with pytest.raises(NotImplementedError):
        fakeElectrometerWithoutInterface.set_aperture_time_min()
    with pytest.raises(NotImplementedError):
        fakeElectrometerWithoutInterface.set_aperture_time_max()
    with pytest.raises(NotImplementedError):
        fakeElectrometerWithoutInterface.set_integration_time_min()
    with pytest.raises(NotImplementedError):
        fakeElectrometerWithoutInterface.set_integration_time_max()
    # Trigger interface
    with pytest.raises(NotImplementedError):
        fakeElectrometerWithoutInterface.set_trigger_count(42)
    with pytest.raises(NotImplementedError):
        fakeElectrometerWithoutInterface.set_trigger_count_min()
    with pytest.raises(NotImplementedError):
        fakeElectrometerWithoutInterface.set_trigger_count_max()
    with pytest.raises(NotImplementedError):
        fakeElectrometerWithoutInterface.get_trigger_count()
    with pytest.raises(NotImplementedError):
        fakeElectrometerWithoutInterface.set_trigger_timer(42)
    with pytest.raises(NotImplementedError):
        fakeElectrometerWithoutInterface.set_trigger_timer_min()
    with pytest.raises(NotImplementedError):
        fakeElectrometerWithoutInterface.set_trigger_timer_max()
    with pytest.raises(NotImplementedError):
        fakeElectrometerWithoutInterface.get_trigger_timer()
