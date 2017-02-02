
.. _help_desk:

Help Desk
=========

The Help Desk is an operative tool used to provide support to FIWARE Lab Users mainly,
although it includes channels for marketing as well, such as Speakers, Mundus, etc.

The complete set of channels is available at https://www.fiware.org/contact-us/.

FIWARE's Help Desk has been built by connecting three tools: Email lists, JIRA trackers and Backlog web site.
All incoming emails are feeding the `HelpDesk Tracker <https://jira.fiware.org/projects/HELP>`_ where they are classified
to their corresponding JIRA holder components and assigned for its resolution.

+---------------------------+--------------------------+--------------------------------+
| Email Channel             | JIRA Component           | Leader                         |
+===========================+==========================+================================+
| fiware-general-help       | `GENERAL-HELP`_          | ATOS - Malena Donato           |
+---------------------------+--------------------------+--------------------------------+
| fiware-speakers-req       | `SPEAKERS-REQ`_          | ATOS - Malena Donato           |
+---------------------------+--------------------------+--------------------------------+
| fiware-feedback           | `FEEDBACK`_              | ENG - Davide dalle Carbonare   |
+---------------------------+--------------------------+--------------------------------+
| fiware-tech-help          | `TECH-HELP`_             | TID - Manuel Escriche          |
+---------------------------+--------------------------+--------------------------------+
| fiware-lab-help           | `LAB-HELP`_              | ENG - Alfonso PietroPaolo      |
+---------------------------+--------------------------+--------------------------------+
| fiware-ops-help           | `OPS-HELP`_              | CREATE - Federico Facca        |
+---------------------------+--------------------------+--------------------------------+
| fiware-collaboration-req  | `COLLABORATION-REQ`_     | ATOS - Malena Donato           |
+---------------------------+--------------------------+--------------------------------+
| fiware-smart-cities-req   | `SMART-CITIES-REQ`_      | TID - Sergio García Gómez      |
+---------------------------+--------------------------+--------------------------------+
| fiware-open-data-req      | `OPEN_DATA-REQ`_         | TID - Sergio García Gómez      |
+---------------------------+--------------------------+--------------------------------+
| fiware-mundus-req         | `MUNDUS-REQ`_            | CREATE - Federico Facca        |
+---------------------------+--------------------------+--------------------------------+

The help desk has also a dedicated section for the accelerators: :ref:`coaches_helpdesk`

.. _GENERAL-HELP: https://jira.fiware.org/secure/IssueNavigator.jspa?reset=true&jqlQuery=project+%3D+HELP+AND+component+%3D+FIWARE-GENERAL-HELP
.. _SPEAKERS-REQ: https://jira.fiware.org/secure/IssueNavigator.jspa?reset=true&jqlQuery=project+%3D+HELP+AND+component+%3D+FIWARE-SPEAKERS-REQ
.. _FEEDBACK: https://jira.fiware.org/secure/IssueNavigator.jspa?reset=true&jqlQuery=project+%3D+HELP+AND+component+%3D+FIWARE-FEEDBACK
.. _TECH-HELP: https://jira.fiware.org/secure/IssueNavigator.jspa?reset=true&jqlQuery=project+%3D+HELP+AND+component+%3D+FIWARE-TECH-HELP
.. _LAB-HELP: https://jira.fiware.org/secure/IssueNavigator.jspa?reset=true&jqlQuery=project+%3D+HELP+AND+component+%3D+FIWARE-LAB-HELP
.. _OPS-HELP: https://jira.fiware.org/secure/IssueNavigator.jspa?reset=true&jqlQuery=project+%3D+HELP+AND+component+%3D+FIWARE-OPS-HELP
.. _COLLABORATION-REQ: https://jira.fiware.org/secure/IssueNavigator.jspa?reset=true&jqlQuery=project+%3D+HELP+AND+component+%3D+FIWARE-COLLABORATION-REQ
.. _SMART-CITIES-REQ: https://jira.fiware.org/secure/IssueNavigator.jspa?reset=true&jqlQuery=project+%3D+HELP+AND+component+%3D+FIWARE-SMART-CITIES-REQ
.. _OPEN_DATA-REQ: https://jira.fiware.org/secure/IssueNavigator.jspa?reset=true&jqlQuery=project+%3D+HELP+AND+component+%3D+FIWARE-OPEN-DATA-REQ
.. _MUNDUS-REQ: https://jira.fiware.org/secure/IssueNavigator.jspa?reset=true&jqlQuery=project+%3D+HELP+AND+component+%3D+FIWARE-MUNDUS-REQ

.. _main_helpdesk:

Main Help Desk
--------------

The main help desk view is provided at http://backlog.fiware.org/helpdesk/

A summary view of the help desk is provided with statistics and two graphs shown in the snapshot below.

Three data set are considered to give statistics parameters about: mean, median, standard deviation

* ALL data set, in black colour
* Created in last 60 days, in green colour
* Pending, in red colour

.. figure:: _static/helpdesk_main_stats.jpg
   :align: center

   Main Help Desk - Summary View

Additionally, each channel has it own statistics at http://backlog.fiware.org/helpdesk/main/stats.

As an example an snapshot about the General Help Channel is shown below:

.. figure:: _static/helpdesk_general_stats.jpg
   :align: center

   General Help Channel - Summary View


Although incoming issues arrive from different email list,
the issue's solver has to allocate it to their right channel by hand.


Lab Channel View
^^^^^^^^^^^^^^^^
There's a public url providing this view at http://backlog.fiware.org/helpdesk/lab

A summary view of the channel is provided with the statistics and graphs.
After identifying the channel, the first three rows provide statistics
for ALL items in the channel (black color), for issues created in last 60 days (green color), and for unresolved issues (red color)

Afterwards, the graph to the left shows evolution in time for created and resolved issues. Emphasizing with a column monthly progress.
The graph to the right displays an histogram with the resolution time for ALL resolved issues and for recent resolved issues (last 60 days).
And it also includes age of unresolved issues.

.. figure:: _static/helpdesk_lab_stats.jpg
   :align: center

Additionally, a list of all unresolved issues is provided so that both users and help desk operators can share the same information.

.. figure:: _static/helpdesk_lab_unresolved.jpg
   :align: center

Finally, a list of recenly resolved issues is shown in order to allow their verfication.

.. figure:: _static/helpdesk_lab_resolved.jpg
   :align: center


Tech Channel View
^^^^^^^^^^^^^^^^^^
There's a public url providing this view at http://backlog.fiware.org/helpdesk/tech

This page follows the same pattern as the Lab Channel View.
A summary view of the channel is provided with the statistics and graphs.
After identifying the channel, the first three rows provide statistics
for ALL items in the channel (black color), for issues created in last 60 days (green color), and for unresolved issues (red color)

Afterwards, the graph to the left shows evolution in time for created and resolved issues. Emphasizing with a column monthly progress.
The graph to the right displays an histogram with the resolution time for ALL resolved issues and for recent resolved issues (last 60 days).
And it also includes age of unresolved issues.

.. figure:: _static/helpdesk_tech_stats.jpg
   :align: center

Additionally, a list of all unresolved issues is provided so that both users and help desk operators can share the same information.

.. figure:: _static/helpdesk_tech_unresolved.jpg
   :align: center

Finally, a list of recenly resolved issues is shown in order to allow their verfication.

.. figure:: _static/helpdesk_tech_resolved.jpg
   :align: center


Enabler Help Desk
^^^^^^^^^^^^^^^^^

GE Owners contribute to support their GEs deployed in FIWARE Lab by answering related questions or by fixing bugs.
In order to help them have better understanding of their related issues and response, a focused view is displayed.

To access it, go to Enablers, then pick up an enabler, and click on Help Desk item in the second menu bar

.. figure:: _static/helpdesk_tech_enabler_menu.jpg
   :align: center

   Menu sequence to access the enabler's help desk page


The enabler help desk page identifies first the enabler: name, owner, ... and its keyword.
Then, the Inbox is displayed with all items collected in the help desk for this GE Owner.
These items are proposed because they can not be filtered properly until its name is fixed.

Therefore, you need to modify its name according to the pattern below to move it from the Inbox to the Enabler Help Desk Box::

    FIWARE.Request.Lab.<Chapter>.<Enabler>.<Item>

Additionally, sometimes issues came from the wrong channel, and there's need to fix it as well.

* Make sure the issues' component is TECH-HELP

When writting <item>, please, take into account:

* It should be short but meaningful.
* Avoid redundancy, like repeating FIWARE, or Lab

.. figure:: _static/helpdesk_tech_enabler.jpg
   :align: center

   Enabler's help desk page




.. _coaches_helpdesk:

Coaches Help Desk
-----------------

FIWARE Help Desk has a section devoted to support accelerators.
This help desk is composed by channels following similar structure to the main helpdesk.
Each channel has its corresponding coach responsible for attending incoming request.

+----------------------------------+--------------------------+--------------------------------+
| Email Channel                    | JIRA Component           | Leader                         |
+==================================+==========================+================================+
| fiware-ceedtech-coaching         | `CEED Tech`_             | CONSOFT - Marco Terrinoni      |
+----------------------------------+--------------------------+--------------------------------+
| fiware-creatifi-coaching         | `CreatiFI`_              | CREATE - Silvio Cretti         |
+----------------------------------+--------------------------+--------------------------------+
| fiware-europeanpioneers-coaching | `EuropeanPioneers`_      | ORANGE - Thierry Nagellen      |
+----------------------------------+--------------------------+--------------------------------+
| fiware-fabulous-coaching         | `FABulous`_              | ENG - Pasquale Vitale          |
+----------------------------------+--------------------------+--------------------------------+
| fiware-fiadopt-coaching          | `FI-ADOPT`_              | ATOS - Omer Ozdemir            |
+----------------------------------+--------------------------+--------------------------------+
| fiware-fic3-coaching             | `FI-C3`_                 | EGLOBALMARK - Franck Le Gall   |
+----------------------------------+--------------------------+--------------------------------+
| fiware-fiche-coaching            | `FICHe`_                 | EGLOBALMARK - Franck Le Gall   |
+----------------------------------+--------------------------+--------------------------------+
| fiware-finish-coaching           | `Finish`_                | ATOS - Omer Ozdemir            |
+----------------------------------+--------------------------+--------------------------------+
| fiware-finodex-coaching          | `FINODEX`_               | ENG - Pasquale Vitale          |
+----------------------------------+--------------------------+--------------------------------+
| fiware-fractals-coaching         | `FRACTALS`_              | ATOS - Omer Ozdemir            |
+----------------------------------+--------------------------+--------------------------------+
| fiware-frontiercities-coaching   | `FrontiersCities`_       | ENG  - Francesco Arigliano     |
+----------------------------------+--------------------------+--------------------------------+
| fiware-impact-coaching           | `IMPACT`_                | TID  - Leandro Guillén         |
+----------------------------------+--------------------------+--------------------------------+
| fiware-incense-coaching          | `INCENSe`_               | ENG  - Pasquale Andriani       |
+----------------------------------+--------------------------+--------------------------------+
| fiware-smartagrifood-coaching    | `SmartAgriFood2`_        | ATOS - Omer Ozdemir            |
+----------------------------------+--------------------------+--------------------------------+
| fiware-soulfi-coaching           | `SOUL-FI`_               | TID  - Leandro Guillén         |
+----------------------------------+--------------------------+--------------------------------+
| fiware-speedup-coaching          | `SpeedUp Europe`_        | TID  - Leandro Guillén         |
+----------------------------------+--------------------------+--------------------------------+

.. _CEED Tech: https://jira.fiware.org/secure/IssueNavigator.jspa?reset=true&jqlQuery=project+%3D+HELC+AND+component+%3D+%22CEED+Tech%22
.. _CreatiFI: https://jira.fiware.org/secure/IssueNavigator.jspa?reset=true&jqlQuery=project+%3D+HELC+AND+component+%3D+CreatiFI
.. _EuropeanPioneers: https://jira.fiware.org/secure/IssueNavigator.jspa?reset=true&jqlQuery=project+%3D+HELC+AND+component+%3D+EuropeanPioneers
.. _FABulous: https://jira.fiware.org/secure/IssueNavigator.jspa?reset=true&jqlQuery=project+%3D+HELC+AND+component+%3D+FABulous
.. _FI-ADOPT: https://jira.fiware.org/secure/IssueNavigator.jspa?reset=true&jqlQuery=project+%3D+HELC+AND+component+%3D+FI-ADOPT
.. _FI-C3: https://jira.fiware.org/secure/IssueNavigator.jspa?reset=true&jqlQuery=project+%3D+HELC+AND+component+%3D+FI-C3
.. _FICHe: https://jira.fiware.org/secure/IssueNavigator.jspa?reset=true&jqlQuery=project+%3D+HELC+AND+component+%3D+FICHe
.. _Finish: https://jira.fiware.org/secure/IssueNavigator.jspa?reset=true&jqlQuery=project+%3D+HELC+AND+component+%3D+Finish
.. _FINODEX: https://jira.fiware.org/secure/IssueNavigator.jspa?reset=true&jqlQuery=project+%3D+HELC+AND+component+%3D+FINODEX
.. _FRACTALS: https://jira.fiware.org/secure/IssueNavigator.jspa?reset=true&jqlQuery=project+%3D+HELC+AND+component+%3D+FRACTALS
.. _FrontiersCities: https://jira.fiware.org/secure/IssueNavigator.jspa?reset=true&jqlQuery=project+%3D+HELC+AND+component+%3D+FrontierCities
.. _IMPACT: https://jira.fiware.org/secure/IssueNavigator.jspa?reset=true&jqlQuery=project+%3D+HELC+AND+component+%3D+IMPACT
.. _INCENSe: https://jira.fiware.org/secure/IssueNavigator.jspa?reset=true&jqlQuery=project+%3D+HELC+AND+component+%3D+INCENSe
.. _SmartAgriFood2: https://jira.fiware.org/secure/IssueNavigator.jspa?reset=true&jqlQuery=project+%3D+HELC+AND+component+%3D+SmartAgriFood2
.. _SOUL-FI: https://jira.fiware.org/secure/IssueNavigator.jspa?reset=true&jqlQuery=project+%3D+HELC+AND+component+%3D+SOUL-FI
.. _SpeedUp Europe: https://jira.fiware.org/secure/IssueNavigator.jspa?reset=true&jqlQuery=project+%3D+HELC+AND+component+%3D+%22SpeedUp+Europe%22


.. figure:: _static/helpdesk_coaches_main.jpg
   :align: center

   Coaches help desk - Summary view


This help desk section has also fresh input about incoming and resolved issues:

.. figure:: _static/helpdesk_coaches_unresolved.jpg
   :align: center

   Coaches help desk - Unresolved Issues

.. figure:: _static/helpdesk_coaches_resolved.jpg
   :align: center

   Coaches help desk - Resolved Issues


And there are summary views for all coaches help desk channels to understand their evolution:

.. figure:: _static/helpdesk_coaches_channel.jpg
   :align: center

   Coaches help desk channel - Summary View

These views are available at http://backlog.fiware.org/helpdesk/coaches/stats

Relationship with Main Help Desk
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

As stated above each accelerator has its own coach to give specific support.
However sometimes the requests received by the coaches are either specific to the node the accelerator is working on
or to the Generic Enabler the accelerator is working with. In these cases the coach doesn't answer the question himself
but to assign it to the corresponding GE Owner or Node support Team.

Assignment to GE owners can be done directly on the coaches help desk but this cannot be done for the nodes. In this case
the issue is cloned to the help desk and assigned to the node support team there.

.. figure:: _static/helpdesk_main_coach_relationship.jpg
   :align: center

   Coaches help desk - Relationship with Main help desk

#. FIWARE developer sends a request to the coaches help desk
#. The coach provides support, assigns it to a GE owner or redirects it to the main help desk
#. The coach redirects the issue to the main help desk by clonning it ( :ref:`jira_issue_clone` ).
   Once in the main help desk it'll be assigned to the corresponding node support team (LAB channel)
#. The Node support team provides support in the :ref:`main_helpdesk`
#. The GE Owner (TECH channel) provides support in the :ref:`coaches_helpdesk`

If the coaches assess the issue was sent to the wrong help desk, he simply :ref:`jira_issue_move` to the main help desk