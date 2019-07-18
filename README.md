# Munki Promoter [![Codacy Badge](https://api.codacy.com/project/badge/Coverage/763edf5e399945378a3b8fd649576a6d)](https://www.codacy.com?utm_source=github.com&utm_medium=referral&utm_content=tcinbis/munkipromoter&utm_campaign=Badge_Coverage)[![Codacy Badge](https://api.codacy.com/project/badge/Grade/763edf5e399945378a3b8fd649576a6d)](https://www.codacy.com?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=tcinbis/munkipromoter&amp;utm_campaign=Badge_Grade)[![Build Status](https://travis-ci.com/tcinbis/munkipromoter.svg?token=UG4L2xzc4VqB7GwMRNRu&branch=master)](https://travis-ci.com/tcinbis/munkipromoter)
Munki Promoter is a tool which manages the lifecycle of your software packages within a 
[Munki](https://github.com/munki/munki) repository automatically. For example you receive new versions of your packages
every couple of days and it goes into a development or testing state where you can evaluate the new package. 
After a predefined period of days and if no complaints or errors were reported these new versions should now be 
promoted to the production state.
Additionally you may want to offer a certain degree of transparency, therefore the current state of your software 
repository is mirrored by a Jira Board, where each issue represents a package.
But not only is the Jira Board a visual representation it also acts as a familiar user interface to change certain
packages options which will be considered by the _Munki Promoter_.

This is the main use case for the _Munki Promoter_.
It loads packages from a existing Munki Repository, creates or updates the corresponding Jira issues and then checks
whether a software package can or should be promoted to another catalog. In this general case we decided to go with a 
three catalog approach.
- Development
- Testing
- Production

For more information and how to set up your version of _Munki Promoter_ please refer to our [documentation](https://tcinbis.github.io/munkipromoter-docs).

## Development & Testing
Bug fixes, documentation improvements or feature requests are always welcome. Please note that we have certain measures
in place to ease development, ensure code quality and readability. Some of them are explained below.

### Black
To ensure consistency in our code we utilise [Black](https://github.com/python/black) as a code formatter.

### Tox
>[Tox](https://tox.readthedocs.io/en/latest/index.html) aims to automate and standardize testing in Python. 
>It is part of a larger vision of easing the packaging, testing and release process of Python software.

To test future compatibility a basic tox configuration is also included in this repo. By simply running `tox` in the
main directory the test can be started.

As the code currently uses certain features from `from __future__ import annotations` the code is only compatible with 
Python version 3.7 and above.  

### Testing & Coverage reports
As a test runner we utilised [pytest](https://pytest.org) and already created tests which aim to cover most of the
critical application modules.

To view the test coverage just run 

```coverage run -m pytest tests/* --cov=. --cov-report=html```

The results will then be stored in a new folder called `htmlcov`. and published on 
[Codacy](https://app.codacy.com/project/tom.cinbis/munkipromoter/dashboard).