# -*- coding: utf-8 -*-
############################################################################
#
# Copyright © 2014 OnlineGroups.net and Contributors.
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
from email.utils import parseaddr
from zope.component import createObject
from gs.group.list.command import CommandResult, CommandABC
from Products.CustomUserFolder.interfaces import IGSUserInfo
from .audit import LeaveAuditor, LEAVE_COMMAND
from .utils import leave_group


class LeaveCommand(CommandABC):
    'The ``unsubscribe`` command.'

    def process(self, email, request):
        'Process the email command ``unsubscribe``'
        components = self.get_command_components(email)
        if components[0] != 'unsubscribe':
            m = 'Not a unsubscribe command: {0}'.format(email['Subject'])
            raise ValueError(m)

        retval = CommandResult.notACommand
        if (len(components) == 1):
            userInfo = self.get_user(email)
            if userInfo:
                groupInfo = createObject('groupserver.GroupInfo',
                                         self.group)
                auditor = LeaveAuditor(self.group, userInfo, groupInfo)
                addr = self.get_email_addr(email)
                auditor.info(LEAVE_COMMAND, addr)

                leave_group(groupInfo, userInfo, request)
            retval = CommandResult.commandStop
        return retval

    @staticmethod
    def get_email_addr(emailMessage):
        retval = parseaddr(emailMessage['From'])[1]
        return retval

    def get_user(self, email):
        retval = None
        sr = self.group.site_root()
        addr = self.get_email_addr(email)
        user = sr.acl_users.get_userByEmail(addr)
        if user:
            retval = IGSUserInfo(user)
        return retval
