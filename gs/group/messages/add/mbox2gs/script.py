# -*- coding: utf-8 -*-
##############################################################################
#
# Copyright © 2013, 2014 OnlineGroups.net and Contributors.
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
from __future__ import unicode_literals, absolute_import
# Standard modules
from argparse import ArgumentParser, FileType
import mailbox
from socket import gaierror
import sys
if (sys.version_info < (3, )):
    from urlparse import urlparse
else:
    from urllib.parse import urlparse  # lint:ok
# GroupServer modules
from gs.config.config import ConfigError
from gs.group.messages.add.smtp2gs.errorvals import exit_vals
from gs.group.messages.add.smtp2gs.servercomms import (NotOk, )
from gs.group.messages.add.smtp2gs.script import (get_token_from_config,
    add_post_to_groupserver)


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


def process_message(uri, listId, emailMessage, token):
    l = len(emailMessage)
    if l == 0:
        m = '5.3.0 The email message was empty.\n'
        sys.stderr.write(m)
        sys.exit(exit_vals['input_file_empty'])

    try:
        add_post_to_groupserver(sys.argv[0], uri, listId, emailMessage, token)
    except gaierror as g:
        m = '4.4.4 Error connecting to the server while processing '\
            'the message:\n%s\n' % (g)
        sys.stderr.write(m)
        sys.exit(exit_vals['socket_error'])
    except NotOk as ne:
        m = '4.5.0 Error communicating with the server while '\
            'processing the message:\n%s\n' % (ne)
        sys.stderr.write(m)
        sys.exit(exit_vals['communication_failure'])
    except ValueError:
        m = '4.5.0 Could not decode the data returned by the server '\
            'while processing the\nmessage. Check the token?\n'
        sys.stderr.write(m)
        sys.exit(exit_vals['json_decode_error'])


def main(configFileName):
    args = get_args(configFileName)
    try:
        token = get_token_from_config(args.instance, args.config)
    except ConfigError as ce:
        m = '4.3.5: Error with the configuration file "%s":\n%s\n' %\
            (args.config, ce.message)
        sys.stderr.write(m)
        sys.exit(exit_vals['config_error'])
    mbox = mailbox.mbox(args.file.name)
    for i, emailMessage in enumerate(mbox):
        if args.verbose:
            m = 'Processing message {0} of {1}\n'.format(i + 1, len(mbox))
            sys.stdout.write(m)
        process_message(args.url, args.listId, str(emailMessage), token)
    sys.exit(exit_vals['success'])
