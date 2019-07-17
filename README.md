# Munki Promoter [![Codacy Badge](https://api.codacy.com/project/badge/Coverage/763edf5e399945378a3b8fd649576a6d)](https://www.codacy.com?utm_source=github.com&utm_medium=referral&utm_content=tcinbis/munkipromoter&utm_campaign=Badge_Coverage) [![Codacy Badge](https://api.codacy.com/project/badge/Grade/763edf5e399945378a3b8fd649576a6d)](https://www.codacy.com?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=tcinbis/munkipromoter&amp;utm_campaign=Badge_Grade) [![Build Status](https://travis-ci.com/tcinbis/munkipromoter.svg?token=UG4L2xzc4VqB7GwMRNRu&branch=master)](https://travis-ci.com/tcinbis/munkipromoter) [![Code style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/tcinbis/munkipromoter)

## Installation and usage
_Munki Promoter_ currently requires Python version 3.7+ and [Munki tools](https://github.com/munki/munki/releases) to be 
installed on the machine running the application code.

Its dependencies can be installed by running `pip install -r requirements.txt`.
Once the prerequisites are satisfied we can begin to add all necessary configuration values.
The configuration is loaded and managed by the `config.py` module. It tries to load all values from the
local environment.
This offers the advantage to simply deploy and manage a machine with a configuration management tool such as 
[ANTS](https://github.com/ANTS-Framework/ants).

## Development & Testing

### Tox
>[Tox](https://tox.readthedocs.io/en/latest/index.html) aims to automate and standardize testing in Python. 
>It is part of a larger vision of easing the packaging, testing and release process of Python software.

To test future compatibility a basic tox configuration is also included in this repo. By simply running `tox` in the
main directory the test can be started.

As the code currently uses certain features from `from __future__ import annotations` the code is only compatible with 
Python version 3.7 and above.  

### Testing & Coverage reports
As a test runner we utilised [pytest](https://pytest.org) and created tests which aim to cover most of the
critical application modules.

To view the test coverage just run 

```coverage run -m pytest tests/* --cov=. --cov-report=html```

The results will then be stored in a new folder called `htmlcov`.

## Todos
- Create and publish an [ANTS](https://github.com/ANTS-Framework/ants) policy for deploying _Munki Promoter_ instances.