
**********************************
Devices implemented in R-testbench
**********************************



R-testbench performs automatic instrument recognition.
Of course, the commands corresponding to the specific model of instrument must be implemented in the package.


What if my instrument is not implemented
========================================

Don't worry, a generic Tool object is instantiated by the package so that you can send command and query data by passing the SCPI commands corresponding to your instrument.
Once your script is working, you have two solutions:

#. extend R-testbench your-self by creating the object corresponding to your instrument (see :ref:`contributing-label`);
#. send your script to a maintainer so that we do not have to start from scratch.



List of instruments implemented
===============================


By manufacturers
----------------

Keysight Technologies
^^^^^^^^^^^^^^^^^^^^^

- B298x series of electrometers

  - B2981A
  - B2983A
  - B2985A
  - B2987A


By families of instruments
--------------------------

Electrometers
^^^^^^^^^^^^^

- Keysight B298x series

  - B2981A
  - B2983A
  - B2985A
  - B2987A
