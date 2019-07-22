External Configuration File
===========================

In the following we will now explore each variable and its purpose.

Promoter
--------
- DEFAULT_PROMOTION_INTERVAL
    TBD

- DEFAULT_PROMOTION_DAY
    TBD

Munki
-----
- REPO_PATH
    TBD
- DEBUG_PKGS_INFO_SAVE_PATH
    TBD
- DRY_RUN
    TBD

Jira
----
- JIRA_URL
    TBD
- JIRA_USER
    TBD
- JIRA_PASSWORD
    TBD
- JIRA_PROJECT_KEY
    TBD
- JIRA_SOFTWARE_NAME_FIELD
    TBD
- JIRA_SOFTWARE_VERSION_FIELD
    TBD
- JIRA_CATALOG_FIELD
    TBD
- JIRA_AUTOPROMOTE_FIELD
    TBD
- _JIRA_AUTOPROMOTE_TRUE
    TBD
- _JIRA_AUTOPROMOTE_FALSE
    TBD
- JIRA_PRESENT_FIELD
    TBD
- JIRA_DEVELOPMENT_TRANSITION_NAME
    TBD
- JIRA_TESTING_TRANSITION_NAME
    TBD
- JIRA_PRODUCTION_TRANSITION_NAME
    TBD

Logger
------
- LOG_LEVEL
    TBD
- LOG_BACKUP_COUNT
    TBD
- LOG_DIR
    TBD
- LOG_FILENAME
    TBD

Default
-------
Below you can see an example configuration of the external configuration file
utilized by *Munki Promoter* in case no environment variables are present.

.. include:: ../src/utils/default.ini
   :literal:

Miscellaneous
-------------
.. warning:: Usually there is no need to change the variables below, but for the
   sake of completeness we will document them here anyway.

- CATALOGS_DIR
    TBD
- PKGS_INFO_DIR
    TBD
- MAKECATALOGS
    TBD
- MAKECATALOGS_PARAMS
    TBD



- JIRA_PROJECT_FIELD
    TBD
- JIRA_ISSUE_TYPE_FIELD
    TBD
- JIRA_ISSUE_TYPE
    TBD
- JIRA_SUMMARY_FIELD
    TBD
- JIRA_DESCRIPTION_FIELD
    TBD
- JIRA_DUEDATE_FIELD
    TBD
- JIRA_LABELS_FIELD
    TBD