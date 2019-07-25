Welcome to Munki Promoter's documentation!
==========================================

Vision & Goals
--------------

This project is a tool to enable the linking of a Jira board together with a
Munki repository. In the beginning, an initial mirror of the Munki repository is
created inside a Jira board. Afterwards the goal is to track the changes made.
On the one hand an end user can interact with the Jira board by manually
promoting a Munki package to another Jira Lane (which represents a Munki
catalog) or to adjust metadata via the Jira interface. On the other hand AutoPkg
adds new packages to the Munki repository. These changes will be recognized
and the Munki Promoter does keep the changes consistent. Jira is always the
single point of truth and the Munki packages are kept inline with it. Only if
new packages are added to the Munki repository the Jira Board will be updated,
but from this point on the package status is only changed by Jira.

Important Features
------------------

- Dry Run
    The Munki Promoter can be run without commiting any changes.
    This enables easier debugging with a consistent state

- Command line interface (CLI)
    The Munki Promoter does support a simple
    commandline interface to configure important environment variables such as
    the dry run, the verbosity, the jira and munki repository and many more

- Unit Tests
    A majority of the code is covered by unit test to make sure future
    extensions do not break the intended functionality

- Logging
    All kind of changes, differences and missing packages are logged to
    the system and to a log file. Furthermore Jira does notify about
    transistions.

- Abstract backend
    The backend is generalized to allow a further extensions such that the tool
    can be extended by other backends than Jira

.. toctree::
   :maxdepth: 3
   :caption: Contents:

   quickstart
   modules


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
