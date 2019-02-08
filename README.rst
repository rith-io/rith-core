.. image::https://travis-ci.org/rith-io/rith-core.svg?branch=master

Arithmetic Framework
====================
Arithmetic helps you create production-ready APIs so that your team can build faster, smarter, and more secure.

Getting Started
---------------
When working with the API source code, it is recommended to create a virtual
environment using `virtualenv`. The API requires your virtual environment to
use Python 3.x.

To create a virtual environment with Python 3 compatibility execute the
following command in the API root.

.. code:: 

  virtualenv -p python3 venv
      
Start Your Virtual Environment
------------------------------
.. code::
  
  source venv/bin/activate

Install Arithmetic
------------------
Now you can install Arithmetic inside of the virtual environment.

.. code::
  
  pip install rith

Contributing
============

If you would like to manually install the API source code, in order to contribute,
please read the CONTRIBUTION GUIDELINES, and ensure that your system has the
required dependencies installed.

Requirements
------------

- Python 3.6+
- Virtualenv
- PostgreSQL with PostGIS

Virtual Environment
-------------------
When working with the API source code, it is recommended to create a virtual
environment using `virtualenv`. The API requires your virtual environment to
use Python 3.x.

To create a virtual environment with Python 3 compatibility execute the
following command in the API root.

.. code::
  
  virtualenv -p python3 venv

Start Development Environment
-----------------------------
.. code::
  
  FLASK_APP=arith:create_application flask run

.. code::
  
  FLASK_APP=arith:create_application\(\"testing\"\) flask run

Manually Generate a PyPi Package
--------------------------------
.. code::
  
  python setup.py sdist bdist_wheel

