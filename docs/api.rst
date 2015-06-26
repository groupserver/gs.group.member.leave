=====================================
:mod:`gs.group.member.leave.base` API
=====================================

.. currentmodule:: gs.group.member.leave.base

The published API for the :mod:`gs.group.member.leave.base`
product consists of the :class:`GroupLeaver` class and the
:func:`leave_group` function.

.. class:: GroupLeaver(groupInfo, userInfo)
           
   Handle leaving a group.

   :param groupInfo: The group the member should leave
   :type groupInfo: :class:`Products.GSGroup.interfaces.IGSGroupInfo`
   :param userInfo: The member leaving the group.
   :type userInfo: :class:`Products.CustomUserFolder.intefaces.IGSUserInfo`

   .. function:: removeMember()

      Remove a member from a group

      :returns: A description of what occurred.
      :rtype: str

      The :func:`GroupLeaver.removeMember` method removes the
      member from the group, and clears the positions that they
      may have had in the group: moderator, group administrator,
      participation coach, and moderated member.

      The email settings of the member are left unchanged.

      .. todo:: posting member, and email settings should be
                cleared?
   
.. function:: leave_group(groupInfo, userInfo, request)

   Utility function to remove someone from a group.

   :param groupInfo: The group the member should leave
   :type groupInfo: :class:`Products.GSGroup.interfaces.IGSGroupInfo`
   :param userInfo: The member leaving the group.
   :type userInfo: :class:`Products.CustomUserFolder.intefaces.IGSUserInfo`
   :param request: The current browser request.
   :type request: :class:`zope.publisher.interfaces.browser.IBrowserRequest`

   The :func:`leave_group` function 

   * Removes the member from a group, 
   * Sends a notification (:doc:`notification`) to the member
     that they have left, and
   * Sends a notification to all the administrators that the
     member has left the group.

Example
=======

The code is not as sophisticated as the Joining User code. The
:class:`GroupLeaver` is instantiated, and the
:func:`GroupLeaver.removeMember` method is called.

.. code-block:: python

  leaver = GroupLeaver(self.groupInfo, self.loggedInUser)
  leaver.removeMember()

More useful is the :func:`leave_group` utility function, which is
used by the user-interfaces to remove a person from a group and
people that the member has left.

.. code-block:: python

  leave_group(self.groupInfo, userInfo, self.request)
