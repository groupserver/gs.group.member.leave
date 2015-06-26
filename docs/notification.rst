=============
Notifications
=============

.. currentmodule:: gs.group.member.leave.base

Two notifications are provided by this product: `you have left`_
and `member has left`_. Both are sent by the :func:`leave_group`
function.

You have left
=============

This notification tells the former member that he or she has
left. It is sent from the **Support** email address, which is
quite important: if it comes from the group that has been left
then it is (highly) likely to be marked as spam. 

The notification is provided by
``gs-group-member-leave-notification.html`` in the *group*
context.

Member has left
===============

This notification is sent to the group administrators telling
them that the member has left. 

The notification is provided by
``gs-group-member-leave-left.html`` in the *group* context.
