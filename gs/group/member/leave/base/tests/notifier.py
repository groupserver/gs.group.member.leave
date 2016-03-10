# -*- coding: utf-8 -*-
############################################################################
#
# Copyright © 2016 OnlineGroups.net and Contributors.
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
from __future__ import absolute_import, unicode_literals, print_function
from mock import (MagicMock, patch, PropertyMock)
from unittest import TestCase
from gs.group.member.leave.base.notifier import (LeftNotifier, )


class TestLeftNotifier(TestCase):

    @patch('gs.group.member.leave.base.notifier.log.warn')
    @patch('gs.group.member.leave.base.notifier.MessageSender.send_message')
    @patch.object(LeftNotifier, 'groupInfo', new_callable=PropertyMock)
    def test_bung_admin(self, m_gI, m_MS_s_m, m_l_w):
        'Test sending a notification to an admin that lacks an email address'
        m_MS_s_m.side_effect = ValueError('Bung')
        groupInfo = m_gI()
        groupInfo.name = 'Example group'
        groupInfo.id = 'eg'
        adminInfo = MagicMock()
        adminInfo.name = 'An Admin'
        adminInfo.id = 'aa'

        l = LeftNotifier(MagicMock(), MagicMock())
        l.adminInfo = adminInfo
        l.subject = 'Ethel the Frog'
        l.text = 'Tonight on Ethel the Frog we look at violence.'
        l.html = '<p>Tonight on Ethel the Frog we look at violence.</p>'
        l.notify()

        m_MS_s_m.assert_called_once_with(l.subject, l.text, l.html)
        self.assertEqual(1, m_l_w.call_count)

    @patch('gs.group.member.leave.base.notifier.log.warn')
    @patch('gs.group.member.leave.base.notifier.MessageSender.send_message')
    @patch.object(LeftNotifier, 'groupInfo', new_callable=PropertyMock)
    def test_admin(self, m_gI, m_MS_s_m, m_l_w):
        'Test sending a notification to an admin that has an email address'
        groupInfo = m_gI()
        groupInfo.name = 'Example group'
        groupInfo.id = 'eg'
        adminInfo = MagicMock()
        adminInfo.name = 'An Admin'
        adminInfo.id = 'aa'

        l = LeftNotifier(MagicMock(), MagicMock())
        l.adminInfo = adminInfo
        l.subject = 'Ethel the Frog'
        l.text = 'Tonight on Ethel the Frog we look at violence.'
        l.html = '<p>Tonight on Ethel the Frog we look at violence.</p>'
        l.notify()

        m_MS_s_m.assert_called_once_with(l.subject, l.text, l.html)
        self.assertEqual(0, m_l_w.call_count)
