.. _faq:

Frequently Asked Questions (FAQ)
===================================

This is a list of Frequently Asked Questions about :ref:`help_desk`, :ref:`backlog`  and :ref:`jira_trackers`.

Feel free to suggest new entries!

#. *How do I remove the sender email address in a help desk issue?*
    You simple take the following steps:

    #. Remove the email address from the description field in the original issue
    #. :ref:`Clone the issue <jira_issue_clone>`
    #. :ref:`Remove the original issue <jira_issue_remove>`

    The cloned issue doesn't keep the historic with the email address inside.

#. *How do I answer an issue in the help desk?*
    Follow the :ref:`jira_email_issue` directions.

#. *How do I request help for internal tools like JIRA, Forge, etc?*
    Yes, we do have an internal help desk for these tools.

    #. :ref:`Create an issue <jira_issue_create>`  in the `Tools Support Desk`_
    #. Select the components you request help for
    #. Put assignee to 'Automatic', this way a notification is sent to the responsible person right away
    #. Define priority or due date, if needed.

#. *How do I request improvements or clarifications for this guide?*

    #. :ref:`Create an issue <jira_issue_create>` in the `Tools Support Desk`_
    #. Select BACKLOG component
    #. Put assignee to 'Automatic'
    #. Define priority or due date, if needed

#. *How do I move an issue to its right channel in the help desk?*

    #. Go to the `HelpDesk Tracker <https://jira.fiware.org/projects/HELP>`_
    #. :ref:`Select the right channel in the issues' component field <jira_issue_component_modify>`.

#. *How do I take an issue from the help desk to my backlog?*

    #. :ref:`Clone the issue <jira_issue_clone>` in the Help Desk
    #. :ref:`Move the issue <jira_issue_move>` to your Tracker and Component
    #. Give it a proper name, according to backlog rules

#. *How do I find the owner of a specific GE?*
    There are a number of alternatives:

    #. Search it at `FIWARE GE/GEri's - R4 & R5 <https://docs.google.com/spreadsheets/d/1rA1E1-Qj866E203h0zcJM9twqt2pku7MS_VAZa9Ngqw/edit#gid=1533683407>`_
    #. Search it at `Backlog Enablers Page <http://backlog.fiware.org/enabler/overview>`_ on the right side.

#. *How do I request help to deploy a GEI on FIWARE LAB?*
    The preferred procedure is:

    #. When creating a work item in LAB Tracker: https://jira.fiware.org/projects/LAB
    #. Allocate it to component: GEI DEPLOYMENT
    #. Assign it to 'Automatic'


.. _Tools Support Desk: https://jira.fiware.org/projects/SUPP