[<img src="https://travis-ci.org/joshuapowell/arith.svg?branch=master" />](https://travis-ci.org/joshuapowell/arith)

# Arith Data API
An open-source geospatial API


# Getting Started

## Manual Installation
If you would like to install the API source code, in order to contribute,
please read the CONTRIBUTION GUIDELINES, and ensure that your system has the
required dependencies installed.

### Requirements

- Python 3.6+
- Virtualenv
- PostgreSQL with PostGIS

### Virtual Environment
When working with the API source code, it is recommended to create a virtual
environment using `virtualenv`. The API requires your virtual environment to
use Python 3.x.

To create a virtual environment with Python 3 compatibility execute the
following command in the API root.

```
virtualenv -p python3 venv
```

### Start Development Environment
```
FLASK_APP=arith:create_application flask run
```

```
FLASK_APP=arith:create_application\(\"testing\"\) flask run
```

### Manually Generate a PyPi Package
```
python setup.py sdist bdist_wheel
```