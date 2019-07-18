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
and **most** importantly for **you** the type of field. These types are critical to the
proper out of the box functioning. In case the types you want to use, differ
from the ones shown below, you need to manually adjust the
:meth:`core.provider.jiraprovider.JiraBoardProvider.commit` method.

.. image:: img/jira-screen-field-types.png
   :scale: 40 %
   :align: center

Find Jira Customfields
----------------------


.. image:: img/jira-issue-inspect.png
   :scale: 25 %
   :align: center

.. image:: img/jira-inspector-html.png
   :scale: 35 %
   :align: center


Jira Workflow & Transitions
----------------------------

Insert into configuration
-------------------------
