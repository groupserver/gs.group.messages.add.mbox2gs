# -*- coding: utf-8 -*-
##############################################################################
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
##############################################################################
from __future__ import unicode_literals
from argparse import ArgumentParser, FileType


def get_args(configFileName):
    p = ArgumentParser(description='Import an mbox file into GroupServer.',
                       epilog='Usually %(prog)s is called to import an .'
                           'mbox file for an entire group, with the -l flag.')
    p.add_argument('url', metavar='url',
                   help='The URL for the GroupServer site.')
    p.add_argument('-l', '--list', dest='listId', default=None,
                   help='The list to send the message to. By default it is '
                       'extracted from the x-original-to header.')
    p.add_argument('-f', '--file', dest='file', default='-',
                   type=FileType('r'),
                   help='The name of the mbox file. If omitted (or '
                       '"%(default)s") standard-input will be read.')
    p.add_argument('-c', '--config', dest='config', default=configFileName,
                   type=str,
                   help='The name of the GroupServer configuration file '
                       '(default "%(default)s") that contains the token that '
                       'will be used to authenticate the script when it tries '
                       'to add each message to the site.')
    p.add_argument('-i', '--instance', dest='instance', default='default',
                   type=str,
                   help='The identifier of the GroupServer instance '
                       'configuration to use (default "%(default)s").')
    p.add_argument('-v', '--verbose', dest='verbose', action='store_true',
                   help='Turn on verbose output. (Normally quiet.)')
    retval = p.parse_args()
    return retval
