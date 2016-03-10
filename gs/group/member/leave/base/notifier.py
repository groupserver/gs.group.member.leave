# -*- coding: utf-8 -*-
############################################################################
#
# Copyright © 2014, 2016 OnlineGroups.net and Contributors.
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
from __future__ import unicode_literals
from logging import getLogger
from zope.component import getMultiAdapter
from zope.i18n import translate
from gs.content.email.base import GroupNotifierABC
from gs.profile.notify import MessageSender
from . import GSMessageFactory as _

#: The logger for the warnings
log = getLogger('gs.group.member.leave.base.notifier')


class LeaveNotifier(GroupNotifierABC):
    htmlTemplateName = 'gs-group-member-leave-notification.html'
    textTemplateName = 'gs-group-member-leave-notification.txt'

    def __init__(self, context, request):
        super(LeaveNotifier, self).__init__(context, request)
        self.__updated = False
        self.htmlTemplate = None
        self.textTemplate = None

    def update(self, groupInfo, userInfo):
        '''Because the user may not have permission to see the group after
he or she has left this ``update`` method allows the notification to be
pre-rendered before it is sent off.'''
        subject = _('leave-notification-subject',
                    'You have left ${groupName}',
                    mapping={'groupName': groupInfo.name})
        self.subject = translate(subject)
        htmlTemplate = getMultiAdapter((self.context, self.request),
                                       name=self.htmlTemplateName)
        self.html = htmlTemplate(userInfo=userInfo)
        textTemplate = getMultiAdapter((self.context, self.request),
                                       name=self.textTemplateName)
        self.text = textTemplate(userInfo=userInfo)

    def notify(self, userInfo):
        sender = MessageSender(self.context, userInfo)
        sender.send_message(self.subject, self.text, self.html)
        self.reset_content_type()


class LeftNotifier(LeaveNotifier):
    htmlTemplateName = 'gs-group-member-leave-left.html'
    textTemplateName = 'gs-group-member-leave-left.txt'

    def update(self, groupInfo, userInfo, adminInfo):
        '''Because the user may not have permission to see the group after
he or she has left this ``update`` method allows the notification to be
pre-rendered before it is sent off.'''
        self.adminInfo = adminInfo
        subject = _('member-left-subject',
                    '${userName} has left ${groupName}',
                    mapping={'userName': userInfo.name,
                             'groupName': groupInfo.name})
        self.subject = translate(subject)
        htmlTemplate = getMultiAdapter((self.context, self.request),
                                       name=self.htmlTemplateName)
        self.html = htmlTemplate(userInfo=userInfo, adminInfo=adminInfo)
        textTemplate = getMultiAdapter((self.context, self.request),
                                       name=self.textTemplateName)
        self.text = textTemplate(userInfo=userInfo, adminInfo=adminInfo)

    def notify(self):
        sender = MessageSender(self.context, self.adminInfo)
        try:
            sender.send_message(self.subject, self.text, self.html)
        except ValueError:  # No email address for the admin
            m = 'Cannot send a "Member has left" notification to the administrator %s (%s) for '\
                'the group %s (%s) on %s (%s) because they lack a verified email address. '\
                'Skipping the notification.'
            log.warn(m, self.adminInfo.name, self.adminInfo.id, self.groupInfo.name,
                     self.groupInfo.id, self.groupInfo.siteInfo.name, self.groupInfo.siteInfo.id)
        else:
            self.reset_content_type()
