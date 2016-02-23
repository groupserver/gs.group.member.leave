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
from gs.group.member.leave.base.leaver import (GroupLeaver, )


class TestGroupLeaver(TestCase):
    '''Test the ``GroupLeaver`` class'''
    @property
    def groupInfo(self):
        retval = MagicMock()
        retval.name = 'Example group'
        retval.id = 'example_group'
        return retval

    @property
    def userInfo(self):
        retval = MagicMock()
        retval.name = 'Dinsdale Parannah'
        retval.id = 'dinsdale'
        return retval

    @patch.object(GroupLeaver, 'isMember', new_callable=PropertyMock)
    @patch.object(GroupLeaver, 'isListedAsAMember', new_callable=PropertyMock)
    @patch.object(GroupLeaver, 'clean_up')
    def test_cleanup(self, m_c_u, m_iLAM, m_iM):
        'Test that we clean up if the user is not a member, but is listed as a member'
        m_iM.return_value = False
        m_iLAM.return_value = True
        ui = self.userInfo
        gl = GroupLeaver(self.groupInfo, ui)
        r = gl.removeMember()

        m_c_u.assert_called_once_with()
        self.assertIn(ui.id, r[0])

    @patch.object(GroupLeaver, 'isMember', new_callable=PropertyMock)
    @patch.object(GroupLeaver, 'isListedAsAMember', new_callable=PropertyMock)
    @patch.object(GroupLeaver, 'remove_all_positions')
    def test_member(self, m_r_a_p, m_iLAM, m_iM):
        'Ensure we try and remove a member'
        m_iM.return_value = True
        m_iLAM.return_value = True
        gi = self.groupInfo
        ui = self.userInfo
        gl = GroupLeaver(gi, ui)
        gl.removeMember()

        m_r_a_p.assert_called_once_with(gi, ui)
        ui.user.del_group.assert_called_once_with(gi.id + '_member')

    @patch.object(GroupLeaver, 'isMember', new_callable=PropertyMock)
    @patch.object(GroupLeaver, 'isListedAsAMember', new_callable=PropertyMock)
    def test_non_member(self, m_iLAM, m_iM):
        'Ensure we ignore non-members'
        m_iM.return_value = False
        m_iLAM.return_value = False
        gi = self.groupInfo
        ui = self.userInfo
        gl = GroupLeaver(gi, ui)
        r = gl.removeMember()

        self.assertEqual([], r)
