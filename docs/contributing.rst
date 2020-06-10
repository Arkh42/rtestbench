
.. _contributing-label:

***************************
Contributing to R-testbench
***************************



Thank you for investing your time in the R-testbench project!

To make the evolution and the history easier to read and to understand, the project follows some rules.
Please read them carefully before contributing.



Commit messages
===============

The first rule is *keep it as short and simple as possible*.

Summarize the main objective of the commit in one line.
If a longer description is necessary, leave a blanck between the summary line and the description.
Synthesize! You may explain the solution to fix an issue, a specific reason to provide a feature that was not available before, and so on.



Types of commits
----------------

Commits can be made for different goals, e.g., organizing the repository or fix a bug.
To enhance the readability of the commit messages, they are organized in several categories.

All commit summary line should start if one of the keyword listed in the table below, sorted alphabetically.

+----------+---------------------------------+-------------------------------------------------------------------+
| KEYWORD  | Description                     | Required information                                              |
+==========+=================================+===================================================================+
|  CHANGE  | Modifies an existing feature.   | Reason for the change.                                            |
+----------+---------------------------------+-------------------------------------------------------------------+
|  DOC     | Modifies the documentation.     | Part of the documentation that is created or updated.             |
+----------+---------------------------------+-------------------------------------------------------------------+
|  FIX     | Fixes a bug or an opened issue. | Reference to issue, if any. Idea/concept/solution used to fix it. |
+----------+---------------------------------+-------------------------------------------------------------------+
|  NEW     | Adds a new feature.             | Description of the proposed feature.                              |
+----------+---------------------------------+-------------------------------------------------------------------+
|  REPO    | Organizes the repository.       | Category of organization concerned by the commit.                 |
+----------+---------------------------------+-------------------------------------------------------------------+



Template for commit message
---------------------------

A typical commit message is::

	KEYWORD one-word goal: summary.

	Long description 
	(if necessary).



Examples
--------

A one-line commit for adding a license::

	REPO license: OSL v3.0
