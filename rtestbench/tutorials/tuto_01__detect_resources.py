
import rtestbench


# Step 1 - create the software remote test bench
testbench = rtestbench.Manager()

# Step 2 - detect available tools
available_tools = testbench.detect_tools()

# Step 3 - print the results
if available_tools:
    print('Available tools:', available_tools)
else:
    print('No available tools')

# Steps 2 and 3 in one command
testbench.print_available_tools()

# Step 4 - close everything properly
testbench.close()
