
***************************
OS supported by R-testbench
***************************



R-testbench is a cross-platform python package.
However, not every distribution of every OS can be tested.


Existing compatibility tests
============================

Currently, existing tests are:

- alpha tester;
- GitHub, an automated workflow for continuous integration with GitHub actions;
- Travis, an automated workflow for continuous integration with `Travis CI`_.

.. _Travis CI: https://travis-ci.org/



Exhaustive list of supported OS
===============================


Here follows an exhaustive table of the OS and specific distribution that have been tested.


+----------------+----------+---------------------+
| Distributions	 | Versions | Tests               |
+================+==========+=====================+
| Windows 10     | N/A      | alpha tester        |
+----------------+----------+---------------------+
| Windows Server | 2019	    | CI (GitHub)         |
+----------------+----------+---------------------+
| Linux Ubuntu   | 18.04    | CI (GitHub)         |
|                +----------+---------------------+
|                | 16.04    | CI (GitHub, Travis) |
+----------------+----------+---------------------+
| macOS          | 10.15    | CI (GitHub)         |
+----------------+----------+---------------------+

