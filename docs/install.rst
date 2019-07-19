Installation
============

Perquisites
-----------

To run *Munki Promoter* please install Python_ 3.7 or above

.. _Python: https://python.org/downloads

Clone Repository
----------------

.. code-block:: bash

   git clone https://github.com/tcinbis/munkipromoter.git


Create virtual environment
--------------------------

.. code-block:: bash

   pip3 install virtualenv
   virtualenv venv --python=python3.7


Install dependencies
--------------------

.. code-block:: bash

   pip install -r requirements.txt

Install *Munki Promoter*
------------------------

.. code-block:: bash

   pip install -e .

Create log file
---------------

.. code-block:: bash

   touch /var/log/munkipromoter.log
   chown <username> /var/log/munkipromoter.log
   chmod 644 /var/log/munkipromoter.log

.. note::
   You may need to adjust the filename of the log in case you defined another
   name in the configuration :mod:`utils.config`.


Now everything should be installed in a way such that we can continue with the
configuration. :doc:`config`