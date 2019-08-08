
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
    rtb.log_warning('Instrument is not locked!')

# [Optional] - enable/disable the display to show/hide the operations
try:
    instr.enable_display()
except RuntimeError as error_msg:
    rtb.log_warning("Instrument's display is not enabled!")
# try:
#     instr.disable_display()
# except RuntimeError as error_msg:
#     rtb.log_warning("Instrument's display is not disabled!")



import time
time.sleep(4)


try:
    instr.config_display_view('roll')
    time.sleep(3)
    instr.config_display_view('graph')
    time.sleep(3)
    instr.config_display_view('hist')
    time.sleep(3)
    instr.config_display_view('meter')
except RuntimeError as error_msg:
    rtb.log_warning("Instrument's display is not enabled!")



# Step x - unlock the device before the end of the script
try:
    instr.unlock()
except RuntimeError as error_msg:
    rtb.log_warning('Instrument is not locked!')



# Step 4 - send raw commands to your resource
# translation_table = dict.fromkeys(map(ord, '\n'), None) # tip to remove newline termination character

# try:
#     id_instr = instr.query('*IDN?') # generic command available for all instruments
#     temperature = instr.query_data(':SYSTem:TEMPerature?') # command specific to Keysight B2895A/B2987A electrometers
# except (UnboundLocalError, RuntimeError) as error_msg:
#     rtb.log_error(error_msg)
# else:
#     rtb.log_info('Instrument ID = {}'.format(id_instr.translate(translation_table)))
#     rtb.log_info('Variable type of Instrument ID is {} because of query()\n'.format(type(id_instr)))
#     rtb.log_info('Temperature = {}'.format(temperature))
#     rtb.log_info('Variable type of Temperature is {} because of query_data()\n'.format(type(temperature)))
