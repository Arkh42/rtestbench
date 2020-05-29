
# R-testbench toolkit
import rtestbench

import sys



# Step 1 - create the software remote test bench
rtb = rtestbench.RTestBench()


# Step 2 - attach the Keysight B2985A to the test bench
ADDR_INSTR = 'USB0::0x0957::0x9318::MY54321248::0::INSTR'

try:
    instr = rtb.attach_resource(ADDR_INSTR)
except ValueError as error_msg:
    rtb.log_critical(error_msg)
    sys.exit('Cannot continue without an instrument... Abort!')
else:
    rtb.log_info('Instrument found. Continue script...')
    

# Step 3 - lock the device
try:
    instr.lock()
except RuntimeError as error_msg:
    rtb.log_error(error_msg)
    rtb.log_warning('Instrument is not locked!')


# [Optional] - enable/disable the display to show/hide the operations
try:
    instr.enable_display()
except RuntimeError as error_msg:
    rtb.log_error(error_msg)
    rtb.log_warning("Instrument's display is not enabled!")
# try:
#     instr.disable_display()
# except RuntimeError as error_msg:
#     rtb.log_warning("Instrument's display is not disabled!")


# Step 4 - configure the view
meas_data_type = ('I', 'Q', 'V', 'R')
view_mode = ('meter', 'graph', 'hist', 'roll')
subview_mode = ('range', 'trigger', 'source', 'roll', 'hist')

x_scale = 10e-6
x_offset = 0
y_scale = 500E-15
y_offset = 0

try:
    instr.config_display_view(view_mode[3])
    instr.config_display_ydata_type(meas_data_type[0])
    instr.config_xscale(x_scale)
    instr.config_xoffset(x_offset)
    instr.config_yscale(y_scale)
    instr.config_yoffset(y_offset)
except RuntimeError as error_msg:
    rtb.log_error(error_msg)
    rtb.log_warning("Instrument's display options are not fully configured!")


# Step 5 - configure the measurements
T_unit = ('celsius', 'kelvin', 'fahrenheit')

try:
    instr.config_temperature_sensor('thermocouple')
    instr.config_temperature_unit(T_unit[0])
    instr.enable_autorange()
    instr.config_aperture_time_min()
    instr.config_output_source_off_cond('default')
    instr.disable_output_source()
except RuntimeError as error_msg:
    rtb.log_error(error_msg)
    rtb.log_warning("Instrument's measurements options are not fully configured!")


# Step 6 - run the measurements
n_meas_points = 100
temperature = None
time = None
current = None
data = None

try:
    instr.timeout = 60e3 # 60 s before throwing Timeout error
    instr.config_result_data_type(['t', 'I'])
    instr.config_trigger_count(n_meas_points)
    instr.config_trigger_timer_min()
    instr.enable_amperemeter()
    temperature = instr.meas_temperature()
    instr.init_meas()
    current = instr.fetch_data('I')
    time = instr.fetch_data('t')
except RuntimeError as error_msg:
    rtb.log_error(error_msg)
    rtb.log_critical("An error occured during measurements run!")
else:
    # Temperature of the system
    if temperature is not None:
        rtb.log_info('Temperature @beginning of measurements run: {} °C.'.format(temperature))
    # Data integrity
    rtb.log_info('Checking data integrity...')
    if time.shape == current.shape:
        rtb.log_info('Checking data integrity...dimensions OK.')
    else:
        rtb.log_warning('Checking data integrity...dimensions mismatch.')
    # Saving data
    if time is not None:
        print('t =', time)
    if current is not None:
        print('I =', current)
finally:
    instr.disable_amperemeter()


# Step 7 - unlock the device before the end of the script
try:
    instr.unlock()
except RuntimeError as error_msg:
    rtb.log_warning('Instrument is not locked!')
