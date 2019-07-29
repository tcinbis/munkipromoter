Installation
============

Prerequisites
-------------

To run *Munki Promoter* please install Python_ 3.7 or above. Additionally you
need to install the munkitools_ on your system to apply changes to pkgsinfo
files. This in turn requires Python 2, but is compatible with the system Python
on Mac.

.. _Python: https://python.org/downloads
.. _munkiTools: https://github.com/munki/munki/releases

Clone Repository
----------------

.. code-block:: bash

   git clone https://github.com/tcinbis/munkipromoter.git


Create virtual environment
--------------------------

.. code-block:: bash

   pip3 install virtualenv
   virtualenv venv --python=python3.7

Activate virtual environment
----------------------------

.. code-block:: bash

   source venv/bin/activate


Install dependencies
--------------------

.. code-block:: bash

   pip install -r munkipromoter/requirements.txt

Install *Munki Promoter*
------------------------

.. code-block:: bash

   pip install ./munkipromoter

Create config file
------------------
*Munki Promoter* includes a default configuration file which you must edit
before you are able to run ``munkipromoter.py``. Simply copy the existing file
located in `src/utils/default.ini` to `/etc/munkipromoter/munkipromoter.ini` and
insert your values there.

Create log file
---------------

.. code-block:: bash

   touch /var/log/munkipromoter.log
   chown <username> /var/log/munkipromoter.log
   chmod 644 /var/log/munkipromoter.log

.. note::
   You may need to use sudo with some commands if the permissions are denied.

.. note::
   You may need to adjust the filename of the log in case you define another
   name in the configuration :mod:`src.utils.config`.


Now everything should be installed in a way such that we can continue with the
configuration. :doc:`config`