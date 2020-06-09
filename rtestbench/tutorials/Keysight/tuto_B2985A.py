
import sys

import rtestbench
from rtestbench.tools.keysight.electrometer import b298x


# Step 1 - create the software remote test bench
testbench = rtestbench.Manager()

# Step 2 - attach the Keysight B2985A to the test bench
ADDR_INSTR = "address"

try:
    electrometer = testbench.attach_tool(ADDR_INSTR)
except ValueError as err:
    testbench.log_error(err)
    testbench.log_critical("Cannot continue without the electrometer... Abort!")
    sys.exit()

# Step 3 - configure the data transfer format
try:
    # electrometer.set_data_transfer_format(tsf_format="text", data_type="fixed-point") # ascii
    # electrometer.set_data_transfer_format(tsf_format="binary", data_type="float") # bin 32
    electrometer.set_data_transfer_format(tsf_format="binary", data_type="double") # bin 64
except RuntimeError as err:
    testbench.log_error(err)
    testbench.log_critical("Electrometer data transfer format is not properly configured!")

# Step 4 - lock the device
try:
    electrometer.lock()
except RuntimeError as err:
    testbench.log_error(err)
    testbench.log_warning("Electrometer is not locked!")

# Step 5 - configure display
try:
    electrometer.set_display(True)
    electrometer.set_view_mode(b298x.KEYSIGHT_B298X_VIEW_MODE_ROLL)
except RuntimeError as err:
    testbench.log_error(err)
    testbench.log_warning("Electrometer's display mode is not fully configured!")


x_scale = 10e-6
x_offset = 0
y_scale = 10E-9
y_offset = 0

try:
    electrometer.set_display_xdata_type(b298x.KEYSIGHT_B298X_MEAS_DATA_TYPE_TIME)
    electrometer.set_xscale(x_scale)
    electrometer.set_xoffset(x_offset)
    electrometer.set_display_ydata_type(b298x.KEYSIGHT_B298X_MEAS_DATA_TYPE_CURRENT)
    electrometer.set_yscale(y_scale)
    electrometer.set_yoffset(y_offset)
except RuntimeError as err:
    testbench.log_error(err)
    testbench.log_warning("Electrometer's display panel is not fully configured!")

# Step 6 - configure the measurements
try:
    electrometer.set_temperature_sensor(b298x.KEYSIGHT_B2985_TEMPERATURE_SENSOR_THERMOCOUPLE)
    electrometer.set_temperature_unit(b298x.KEYSIGHT_B2985_TEMPERATURE_UNIT_CELSIUS)
except RuntimeError as err:
    testbench.log_error(err)
    testbench.log_warning("Electrometer's temperature sensing is not fully configured!")

try:
    electrometer.disable_output_source()
    electrometer.set_output_source_off_condition(b298x.KEYSIGHT_B2985_OUTPUT_SOURCE_OFFCONDITION_NORMAL)
except RuntimeError as err:
    testbench.log_error(err)
    testbench.log_warning("Electrometer's output source is not fully configured!")

try:
    electrometer.set_meas_data_types([
        b298x.KEYSIGHT_B298X_MEAS_DATA_TYPE_TIME,
        b298x.KEYSIGHT_B298X_MEAS_DATA_TYPE_CURRENT,
        b298x.KEYSIGHT_B298X_MEAS_DATA_TYPE_TEMPERATURE
    ])
    electrometer.set_autorange(True)
    electrometer.set_aperture_time_min()
except RuntimeError as err:
    testbench.log_error(err)
    testbench.log_warning("Electrometer's measurement conditions are not fully configured!")

try:
    electrometer.set_trigger_source(b298x.KEYSIGHT_B298X_TRIGGER_SOURCE_TIMER)
    electrometer.set_trigger_count(10)
    electrometer.set_trigger_timer_min()
except RuntimeError as err:
    testbench.log_error(err)
    testbench.log_warning("Electrometer's trigger method is not fully configured!")

# Step 7 - run measurements
try:
    electrometer.enable_amperemeter()
    electrometer.initiate_measurement()
    current = electrometer.fetch_data(b298x.KEYSIGHT_B298X_MEAS_DATA_TYPE_CURRENT)
    time = electrometer.fetch_data(b298x.KEYSIGHT_B298X_MEAS_DATA_TYPE_TIME)
    temperature = electrometer.fetch_data(b298x.KEYSIGHT_B298X_MEAS_DATA_TYPE_TEMPERATURE)
except RuntimeError as err:
    testbench.log_error(err)
    testbench.log_critical("Something went wrong during measurement!")
else:
    print("t =", time)
    print("I =", current)
    print("TEMP =", temperature)
finally:
    electrometer.disable_amperemeter()

# Step 8 - unlock the device before the end of the script
try:
    electrometer.unlock()
except RuntimeError as error_msg:
    testbench.log_warning("Instrument is not unlocked!")

# Step 9 - close everything properly
testbench.close()
