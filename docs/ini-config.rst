External Configuration File
===========================

In the following we will now explore each variable and its purpose.

Promoter
--------
- DEFAULT_PROMOTION_INTERVAL
    This describes the number of days a package stays in one catalog before it
    will be automatically promoted to the next catalog until it is in
    production.

- DEFAULT_PROMOTION_DAY
    Name of the weekday we want to promote on. For example if we set it to
    ``Thursday`` packages will only be promoted after the given time interval
    **and** if it is the correct weekday. Otherwise the package's catalog remain
    unchanged. This is usefull if you want to maintain a regular release
    schedule.

Munki
-----
- REPO_PATH
    The path to the munki repository containing your pkgsinfo and catalogs
    files. It must be present or mounted upon runtime.

- DEBUG_PKGS_INFO_SAVE_PATH
    For debugging purposes all pkgsinfo files can also be written to a custom
    directory instead of overwriting the existing originals in the repository.
    Make sure that the path you specify exists and is actually accessible by the
    user running the *munkipromoter.py*.

- DRY_RUN
    In case *dry run* is enabled in the configuration file or via the command
    line interface no changes will be made to the provider's resources. In our
    case this means no Jira issues will be updated and no Munki pkgsinfo files
    will be overwritten. This is especially useful when debugging code, because
    the code behaves exactly the same except for the
    :func:`core.base_classes.Provider.commit()` method.

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