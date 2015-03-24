# -*- coding: utf-8 -*-
############################################################################
#
# Copyright © 2015 OnlineGroups.net and Contributors.
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
from mock import (MagicMock, patch)
import os.path
from unittest import TestCase
from gs.group.messages.add.mbox2gs.script import (main, process_message)
import gs.group.messages.add.mbox2gs.script as gsscript


class TestScript(TestCase):
    tokenValue = 'tokenValue'
    prefix = 'not-the-actual-prefix'

    def setUp(self):
        gsscript.get_token_from_config = MagicMock(
            return_value=self.tokenValue)
        gsscript.get_relay_address_prefix_from_config = MagicMock(
            return_value=self.prefix)

    @patch.object(gsscript, 'get_args')
    @patch.object(gsscript, 'add_post_to_groupserver')
    def test_mbox_single(self, m_add_post, m_get_args):
        'Test an mbox with a single email message in the file'
        mboxFilename = 'single.mbox'
        args = m_get_args()
        args.file.name = os.path.join(
            'gs', 'group', 'messages', 'add', 'mbox2gs', 'tests',
            mboxFilename)
        args.verbose = False

        with self.assertRaises(SystemExit):
            main('fake-name.cfg')

        self.assertEqual(1, m_add_post.call_count)

    @patch.object(gsscript, 'get_args')
    @patch.object(gsscript, 'add_post_to_groupserver')
    def test_mbox_multiple(self, m_add_post, m_get_args):
        'Test an mbox with multiple email messages in the file'
        mboxFilename = 'multiple.mbox'
        args = m_get_args()
        args.file.name = os.path.join(
            'gs', 'group', 'messages', 'add', 'mbox2gs', 'tests',
            mboxFilename)
        args.verbose = False

        with self.assertRaises(SystemExit):
            main('fake-name.cfg')

        self.assertEqual(2, m_add_post.call_count)

    @patch.object(gsscript, 'add_post_to_groupserver')
    def test_empty_message(self, m_add_post):
        'Test that we do the right thing with an empty message'
        with self.assertRaises(SystemExit) as se:
            process_message('http://groups.example.com', 'list', '',
                            self.tokenValue, self.prefix)

        self.assertNotEqual(0, se.exception.code)
        self.assertEqual(0, m_add_post.call_count)
