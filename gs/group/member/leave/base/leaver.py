# -*- coding: utf-8 -*-
############################################################################
#
# Copyright © 2010, 2011, 2012, 2013, 2014 OnlineGroups.net and
# Contributors.
#
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
############################################################################
from __future__ import absolute_import, unicode_literals
from zope.event import notify
from gs.group.member.base import (member_id, user_member_of_group, get_group_userids)
from gs.group.member.manage.utils import (removePtnCoach, removeAdmin,
                                          unmoderate)
from gs.group.member.manage.utils import (removePostingMember,
                                          removeModerator)
from Products.GSGroupMember.groupMembersInfo import GSGroupMembersInfo
from Products.GSGroupMember.groupmembershipstatus import (
    GSGroupMembershipStatus)
from .audit import LeaveAuditor, LEAVE
from .event import GSLeaveGroupEvent


class GroupLeaver(object):
    def __init__(self, groupInfo, userInfo):
        self.groupInfo = groupInfo
        self.userInfo = userInfo

    def __bool__(self):
        return bool(self.isMember)

    def __nonzero__(self):
        return self.__bool__()

    @property
    def isMember(self):
        # Deliberately not an @Lazy property (the membership will change).
        retval = user_member_of_group(self.userInfo, self.groupInfo)
        return retval

    @property
    def isListedAsAMember(self):
        memberIds = get_group_userids(self.groupInfo.groupObj,
                                      self.groupInfo)
        retval = self.userInfo.id in memberIds
        return retval

    def clean_up(self):
        '''Sometimes group membership can get... odd. Remove them, by hook or by crook'''
        acl_users = self.groupInfo.groupObj.site_root().acl_users
        usergroupName = member_id(self.groupInfo.id)
        group = acl_users.getGroupById(usergroupName)
        group._delUsers((self.userInfo.id,))

    def removeMember(self):
        retval = []
        if (not self.isMember):
            if self.isListedAsAMember:
                self.clean_up()
                m = 'cleaned up odd member {0} ({1})'
                msg = m.format(self.userInfo.name, self.userInfo.id)
                retval.append(msg)
            return retval

        usergroupName = member_id(self.groupInfo.id)
        retval = self.remove_all_positions(self.groupInfo, self.userInfo)
        self.userInfo.user.del_group(usergroupName)
        groupObj = self.groupInfo.groupObj
        if not self.isMember:
            auditor = LeaveAuditor(groupObj, self.userInfo, self.groupInfo)
            auditor.info(LEAVE)
            retval.append('removed from the group')
        notify(GSLeaveGroupEvent(groupObj, self.groupInfo, self.userInfo))
        return retval

    @staticmethod
    def remove_all_positions(groupInfo, userInfo):
        retval = []
        membersInfo = GSGroupMembersInfo(groupInfo.groupObj)
        status = GSGroupMembershipStatus(userInfo, membersInfo)
        if status.isPtnCoach:
            retval.append(removePtnCoach(groupInfo)[0])
        if status.isGroupAdmin:
            retval.append(removeAdmin(groupInfo, userInfo))
        if status.postingIsSpecial and status.isPostingMember:
            retval.append(removePostingMember(groupInfo, userInfo))
        if status.isModerator:
            retval.append(removeModerator(groupInfo, userInfo))
        if status.isModerated:
            retval.append(unmoderate(groupInfo, userInfo))
        return retval
