Usage
=====

In a perfect world you only need to run :mod:`munkipromoter` and it works.
As this is most of the time not the case a simple command line interface offered
to quickly overwrite some of the important configuration values as seen in the
following.

.. code-block:: none

    munkipromoter.py
    usage: munkipromoter.py [-h] [-m REPO_PATH] [-v] [-n] [-j JIRA_URL]
                            [-u JIRA_USER] [-p JIRA_PASSWORD]

    optional arguments:
      -h, --help            show this help message and exit
      -m REPO_PATH, --munki-repo REPO_PATH
      -v, --verbose
      -n, --dry-run
      -j JIRA_URL, --jira-server JIRA_URL
      -u JIRA_USER, --user JIRA_USER
      -p JIRA_PASSWORD, --password JIRA_PASSWORD
