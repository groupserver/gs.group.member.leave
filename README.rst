==============================
``gs.group.member.leave.base``
==============================
~~~~~~~~~~~~~~~~~~~~~~~~~
Leave a GroupServer group
~~~~~~~~~~~~~~~~~~~~~~~~~

:Author: `Michael JasonSmith`_
:Contact: Michael JasonSmith <mpj17@onlinegroups.net>
:Date: 2015-06-26
:Organization: `GroupServer.org`_
:Copyright: This document is licensed under a
  `Creative Commons Attribution-Share Alike 4.0 International License`_
  by `OnlineGroups.net`_.

..  _Creative Commons Attribution-Share Alike 4.0 International License:
    http://creativecommons.org/licenses/by-sa/4.0/

Introduction
============

This product provides the code deals with group members leaving
GroupServer_ groups, whether voluntarily or as the result of an
administrator's action.

A *Leave* page, ``leave.html`` in the **groups** context, is
provided, where a member who wishes to leave is shown advice on
rejoining, given the means to reduce the amount of email received
from the group, and the ability to leave.

Two notifications are provided by this product:

* You have left: ``gs-group-member-leave-notification.html``
* Member has left: ``gs-group-member-leave-left.html``

The actual leaving code is separate from the page, so that it can
be called by other modules. This code also ensures that all
group-membership roles are removed from the member at the time of
leaving, and takes care of auditing the leave event.

Resources
=========

- Documentation:
  http://groupserver.readthedocs.org/projects/gsgroupmemberleavebase
- Code repository:
  https://github.com/groupserver/gs.group.member.leave.base/
- Questions and comments to
  http://groupserver.org/groups/development
- Report bugs at https://redmine.iopen.net/projects/groupserver

.. _GroupServer: http://groupserver.org/
.. _GroupServer.org: http://groupserver.org/
.. _OnlineGroups.Net: https://onlinegroups.net
.. _Michael JasonSmith: http://groupserver.org/p/mpj17

..  LocalWords:  html
