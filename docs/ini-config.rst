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
    :func:`src.core.base_classes.Provider.commit()` method.

Jira
----
- JIRA_URL
    The Jira url is the direct URL to your Jira server instance.

    .. note:: Only the base URL is required here. **NOT** the complete link to
       your specific project.

- JIRA_USER
    The username which the *Munki Promoter* shall use to login to. It must have
    the correct permission to be able to see, edit and move all issues in your
    project. Otherwise Jira will return error codes such as `403`.

- JIRA_PASSWORD
    Corresponding password to the user you want to use.

- JIRA_PROJECT_KEY
    This is the project key which is unique per instance. You can usually find
    the key by looking at the ID of one of the issues you created. For example
    one of our issues is called ``SWPM-140``. In this case the project key is
    ``SWPM``.

- JIRA_SOFTWARE_NAME_FIELD
    Field to display the software name of a package.
    To be able to access the correct field in the Jira issue, we need to know
    the internal name of this field. An example for such a field name would be
    ``customfield_12005``. How to find the names and IDs of fields is described in
    :ref:`find-custom-fields`.

- JIRA_SOFTWARE_VERSION_FIELD
    Field to display the software version of a package.
    To be able to access the correct field in the Jira issue, we need to know
    the internal name of this field. An example for such a field name would be
    ``customfield_12005``. How to find the names and IDs of fields is described in
    :ref:`find-custom-fields`.

- JIRA_CATALOG_FIELD
    Field to display the current catalog a package is in.
    To be able to access the correct field in the Jira issue, we need to know
    the internal name of this field. An example for such a field name would be
    ``customfield_12005``. How to find the names and IDs of fields is described in
    :ref:`find-custom-fields`.

- JIRA_AUTOPROMOTE_FIELD
    Field to display whether to automatically promote a package or not.
    To be able to access the correct field in the Jira issue, we need to know
    the internal name of this field. An example for such a field name would be
    ``customfield_12005``. How to find the names and IDs of fields is described in
    :ref:`find-custom-fields`.

- _JIRA_AUTOPROMOTE_TRUE
    This describes the ``TRUE`` ID for the autopromote field. For example
    ``12003``.
    Because the autopromote field described above is a radio button field we can
    not simply assign an arbitrary value to it. We need to know the different
    IDs of these radio selections.
    How to find the names and IDs of fields is described in
    :ref:`find-custom-fields`.

- _JIRA_AUTOPROMOTE_FALSE
    This describes the ``FALSE`` ID for the autopromote field. For example
    ``12004``.
    Because the autopromote field described above is a radio button field we can
    not simply assign an arbitrary value to it. We need to know the different
    IDs of these radio selections.
    How to find the names and IDs of fields is described in
    :ref:`find-custom-fields`.

- JIRA_PRESENT_FIELD
    Field to display if a package is present in the Munki repository or if it is
    missing.
    To be able to access the correct field in the Jira issue, we need to know
    the internal name of this field. An example for such a field name would be
    ``customfield_12005``. How to find the names and IDs of fields is described in
    :ref:`find-custom-fields`.

- JIRA_DEVELOPMENT_TRANSITION_NAME
    This field should contain the name of the transition to move **any** ticket
    into the development lane on the Jira board.
    How to find the corresponding names is described in :ref:`jira-workflow`.

- JIRA_TESTING_TRANSITION_NAME
    This field should contain the name of the transition to move **any** ticket
    into the testing lane on the Jira board.
    How to find the corresponding names is described in :ref:`jira-workflow`.

- JIRA_PRODUCTION_TRANSITION_NAME
    This field should contain the name of the transition to move **any** ticket
    into the production lane on the Jira board.
    How to find the corresponding names is described in :ref:`jira-workflow`.

Logger
------
- LOG_LEVEL
    The log level to be used when logging to the console.

- LOG_BACKUP_COUNT
    The number of backup logs to keep before rotating.

- LOG_DIR
    The directory where the logfile is written.

- LOG_FILENAME
    The name of the logfile.

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
    Name of the folder where the catalogs are stored in. This is usually called
    ``catalogs``.

- PKGS_INFO_DIR
    Name of the folder where the pkgsinfo files are stored in. This is usually
    called ``pkgsinfo``.

- MAKECATALOGS
    The path of the ``makecatalogs`` tool which needs to be installed locally.
    Default is ``/usr/local/munki/makecatalogs``.

- MAKECATALOGS_PARAMS
    Additional parameters which should be passed to the ``makecatalogs``
    command.



- JIRA_PROJECT_FIELD
    Default field name to find and set the project.
- JIRA_ISSUE_TYPE_FIELD
    Default field name to find and set the issue type.
- JIRA_ISSUE_TYPE
    Default name to set the correct issue type.
- JIRA_SUMMARY_FIELD
    Default field name to find and set the summary.
- JIRA_DESCRIPTION_FIELD
    Default field name to find and set the description.
- JIRA_DUEDATE_FIELD
    Default field name to find and set the due date.
- JIRA_LABELS_FIELD
    Default field name to find and set labels.