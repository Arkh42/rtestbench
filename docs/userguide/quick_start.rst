
***********
Quick start
***********



R-testbench is provided under the ``rtestbench`` Python package.
So, the first step consists in importing rtestbench.

Then, you must instantiate the manager, provided by the ``RTestBenchManager`` class.

Afterwards, you can attach any tool to the virtual test bench to start the remote control.
You set up your virtual test bench as you set up an actual bench, depending on your application.

Finally, you close the test bench to stop your application properly.

That's it!


The quick start code example follows here below:

.. code-block:: python

	import rtestbench
	
	testbench = rtestbench.RTestBenchManager()
	# or, alternatively
	testbench = rtestbench.Manager()
	
	instrument = testbench.attach_tool("instrument address here")
	
	# *** your code here ***
	
	testbench.close()
