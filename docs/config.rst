Configuration
=============

Set up Jira Board
-------------------------

.. image:: img/jira-board-overview.png
   :scale: 20%
   :align: center

.. image:: img/jira-issue.png
   :scale: 25 %
   :align: center

Required Issue fields
---------------------

For the *Munki Promoter* to work properly, we need a minimum set of system and
custom fields for our Jira Issue Type. These fields should be added to the
`Create`, `Edit` and `View` screen in your project configuration.

The fields we need are the following:

- Software Name
- Software Version
- Due date
- Catalog
- Autopromote
- Present

Below you can see an example of such an screen with the fields we need to add
and **most importantly for you** the type of field. These types are critical to the
proper out of the box functioning. In case the types you want to use, differ
from the ones shown below, you need to manually adjust the
:meth:`core.provider.jiraprovider.JiraBoardProvider.commit` method.

.. image:: img/jira-screen-field-types.png
   :scale: 40 %
   :align: center

Find Jira Customfields
----------------------

For the configuration stored in :class:`utils.config.MunkiPromoterConfig` we
need to know the name of each customfield and the corresponding id of the
possible values. These information can unfortunately not be queried
automatically in an easy way yet. Therefore one must open a Jira Issue in his
favourite Web Browser (below we used Firefox) and extract these information from
the html source.


.. image:: img/jira-issue-inspect.png
   :scale: 25 %
   :align: center

Select a field you want to collect the information for and click on the edit
button of this field to change its value. **Before** actually changing the value
you can then right-click on one of the values and open your developer view
(for Firefox the tool is called Inspector). In the screenshot below you can then
see the following three information we need in case of the `Autopromote` field.

.. image:: img/jira-inspector-html.png
   :scale: 35 %
   :align: center

- field name: ``customfield_12701``

- radio option one: ``12003``

- radio option two: ``12004``

These information can now be added to the :mod:`utils.config`. For this example
you would need to set the following configuration options:

- ``JIRA_AUTOPROMOTE_FIELD`` to ``customfield_12701``
- ``_JIRA_AUTOPROMOTE_TRUE`` to ``12003``
- ``_JIRA_AUTOPROMOTE_FALSE`` to ``12004``

Jira Workflow & Transitions
----------------------------

Insert into configuration
-------------------------
