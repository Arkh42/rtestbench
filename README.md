
R-testbench
===========



**R-testbench** is a toolkit written in Python that allows the user to 
create a software remote test bench to control an actual electronic test bench remotely.
It relies on the VISA protocol ([Virtual Instrument Software Architecture](http://www.ni.com/visa/)).
The implementation is built on top of [PyVISA](https://pyvisa.readthedocs.io/en/latest/).



Quick start
-----------


To use **R-testbench**, you simply need to import the *rtestbench* Python package.
```python
import rtestbench
```

Tutorial scripts are available [here](./rtestbench/tutorials/).
This is a user-friendly way to start with the toolkit.



Current status
--------------


Until now, **R-testbench** has been developed to control the Keysight B2985A Electrometer.
However, I built the whole software architecture so that it can be extended to any instrument from any manufacturer.

If you would like to contribute to the project,
please read the [contribution guidelines](https://github.com/Arkh42/rtestbench/blob/master/CONTRIBUTING.md).
You can also contact me by [email](mailto:aquenon@hotmail.be).
