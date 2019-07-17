# Munki Promoter v2

## Quick start

### Dependencies
To install all required packages just run `pip3 install -r requirements.txt`.

### Run tox
[Tox](https://tox.readthedocs.io/en/latest/index.html) aims to automate and standardize testing in Python. It is part of a larger vision of easing the packaging, testing and release process of Python software.

It can be run by executing the command 
`tox` in the `munkipromoter` directory.

### Test Coverage
To view the test coverage just run `coverage run -m pytest tests/* --cov=. --cov-report=html`