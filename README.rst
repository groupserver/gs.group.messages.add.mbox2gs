=================================
``gs.group.messages.add.mbox2gs``
=================================
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Import an ``mbox`` archive into GroupServer
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

:Authors: `Marek Kuziel`_; `Michael JasonSmith`_;
:Contact: Michael JasonSmith <mpj17@onlinegroups.net>
:Date: 2014-05-05
:Organization: `GroupServer.org`_
:Copyright: This document is licensed under a
  `Creative Commons Attribution-Share Alike 4.0 International License`_
  by `OnlineGroups.Net`_.

Introduction
============

This is the code for the `mbox2gs`_ script, which allows to
import email messages from ``mbox`` archives to GroupServer_.  It
can be used for migration of Mailman_ mailing-list archives ie. to
migrate old mailing-lists from Mailman to Groupserver.

This document is intended for advanced users only. **Do not**
attempt to use this unless you are really sure you know what you
are doing! You have been warned.

Before You Start
================

The following describes all steps before ``mbox2gs`` can be called.


1. **(Optional)** Disable SMTP (sending emails) in your
   GroupServer instance. You can disable SMTP in one of two ways.

   i. Modify ``parts/instance/etc/gsconfig.ini`` in your
      GroupServer installation

      - In ``gsconfig.ini`` you have sections
        ``[config-default]``, which has set ``smtp = on`` by
        default. Set ``smtp = off``.

      - Stop and start again your instance so the configuration
        change takes effect.

      - Test sending of email via your GroupServer instance. No
        message should be sent.

   ii. Re-configure your GroupServer instance to use Python's
       native SMTP daemon running in debug mode:

       - SMPT port set to 2525 in ``config.cfg``

       - Run Buildlout::

          $ buildout -N

       - Start the server::

          $ sudo python -m smtpd -n -c DebuggingServer localhost:2525

       - Test sending of email via your GroupServer instance. No
         message should be sent, but you should see the email in
         the DebuggingServer that you are running.

:Important: You may want to disable SMTP in your GroupServer
            instance while you are testing, or even migrating
            archivesd from old Mailman mailin-lists, because
            every email you import would be send to your mailing
            list members.  Which is something you may not want to
            do.

2. Prepare Mailman archives for migration.

   Long story short, things are not in ideal shape in any Mailman
   archive out there, because:

   - Email addresses are usually obfuscated (eg. *some.email at
     example.com*, *some.email*).

   - A typical Mailman archive (usually gzipped) is not a proper
     mbox file.

   The ``mailman2mbox`` Python script deals with the issues and
   helps you to convert your Mailman archives to mbox format
   <https://gist.github.com/wcdolphin/1728592>.


3. Create a new GroupServer group to which you intend to import
   mbox archive(s) in to.

   Example: <http://example.org/groups/my-group/>


4. Get a list of all email addresses from your Mailman
   mailing-list, or extract the list from mbox archives.

5. Load all email addresses to the group via
   ``admin_join_add_csv.html`` page.

   Example: http://example.org/groups/my-group/admin_join_add_csv.html

   :Note: Unless you disable SMTP everyone on the list will get
          an email about the fact that you added them to the
          group.


6. All prepared. You are now ready to migrate your ``mbox``
   archive(s) using ``mbox2gs``.


``mbox2gs``
===========

Usually an advanced user of Groupserver calls ``mbox2gs`` when required to add 
email messages from mbox archive to a GroupServer group. 

``mbox2gs`` is defined as an entry point [#entryPoint]_ to this module.


Usage
-----

::

   mbox2gs [-h] [-v] [-l LISTID] [-f FILE] [-c CONFIG] [-i INSTANCE] url

Positional Arguments
~~~~~~~~~~~~~~~~~~~~

``url``:
  The URL for the GroupServer site.

Optional Arguments
~~~~~~~~~~~~~~~~~~

``-h``, ``--help``:
  Show a help message and exit.

``-v``, ``--verbose``:
  Turn on verbose output. (Normally quiet.)

``-l LISTID``, ``--list LISTID``:
  The list to send the message to. By default it is extracted
  from the ``x-original-to`` header.

``-f FILE``, ``--file FILE``:
  The name of the file that contains the mbox archive. Only one
  archive can be imported at the time. If omitted (or ``-``)
  standard-input will be read.


``-c CONFIG``, ``--config CONFIG``:
  The name of the GroupServer `configuration file`_ (default
  ``$INSTANCE_HOME/etc/gsconfig.ini``) that contains the token
  that will be used to authenticate the script when it tries to
  add the email to the site.

``-i INSTANCE``, ``--instance INSTANCE``:
  The identifier of the GroupServer instance configuration to use (default
  "default").

Returns
-------

The script returns ``0`` on success, or a non-zero on an
error. In the case of an error, ``mbox2gs`` follows the
convention specified in ``/usr/include/sysexits.h``. In addition
the error message that is written to ``stderr`` starts with the
enhanced mail system status code [#rfc3463]_. See `smtp2gs`_ for more information.

Examples
--------

Import the mbox archive stored in ``/tmp/test.mbox`` into the
group ``my_group`` that is on the site ``groups.example.com``,
and produce verbose output::

  mbox2gs -v -l my_group -f /tmp/test.mbox http://groups.example.com


The Code
--------

The ``mbox2gs`` script is provided by the module
``gs.group.messages.add.mbox2gs.script``. The ``main`` function
takes the name of the default configuration file a single
argument, which is normally supplied by ``buildout`` when it
generates the ``mbox2gs`` script from the entry point.

The script parses the command-line arguments, and calls two further functions:

``gs.group.messages.add.smtp2gs.servercomms.get_group_info_from_address``:
  This calls the page ``/gs-group-messages-add-group-exists.html`` to check
  if the group exists, and to get some information about the group.

``gs.group.messages.add.smtp2gs.servercomms.add_post``:
  This calls the page ``/gs-group-messages-add-email.html`` to actually add
  the post.

Both pages are provided by the ``gs.group.messages.add.base`` module
[#add]_; the data is sent by the ``gs.form.post_multipart`` function
[#form]_, with ``gs.auth.token`` [#auth]_ providing authentication (see the
section `Configuration File`_ below).

Configuration File
==================

The configuration for the ``mbox2gs`` script is handled by the
``gs.config`` module [#config]_. It is entirely concerned with token
authentication [#auth]_. To authenticate script needs to pass a token to
the web pages that are used to add a post [#add]_. The pages compare the
token that was passed in to one that is stored in the database. If they
match the script is allowed to post.

Examples
--------

Below is the configuration of the token for the GroupServer instance
``default``::

  [webservice-default]
  token = theValueOfTheToken

A more complex system, which has separate ``testing`` and ``production``
environments::

  [config-testing]
  ...
  webservice = testing

  [config-production]
  ...
  webservice = production

  [webservice-testing]
  token = theValueOfTheTokenForTesting

  [webservice-production]
  token = theValueOfTheTokenForProduction

The token-configuration for two separate sites (accessed through different
URLs) that are supported by the same database::

  [config-firstSite]
  ...
  webservice = default

  [config-secondSite]
  ...
  webservice = default

  [webservice-default]
  token = theValueOfTheDefaultToken

Resources
=========

- Code repository:
  https://source.iopen.net/groupserver/gs.group.messages.add.mbox2gs
- Questions and comments to http://groupserver.org/groups/development
- Report bugs at https://redmine.iopen.net/projects/groupserver

.. _GroupServer: http://groupserver.org/
.. _GroupServer.org: http://groupserver.org/
.. _OnlineGroups.Net: https://onlinegroups.net
.. _Marek Kuziel: http://groupserver.org/p/marek
.. _Michael JasonSmith: http://groupserver.org/p/mpj17
.. _Creative Commons Attribution-Share Alike 4.0 International License:
    http://creativecommons.org/licenses/by-sa/4.0/

.. [#entryPoint] See `Feature 3539 <https://redmine.iopen.net/issues/3539>`_
.. [#rfc3463] `RFC 3463: Enhanced Mail System Status Codes 
             <http://tools.ietf.org/html/rfc3463>`_
.. [#add] See ``gs.group.messages.add.base`` 
            <https://source.iopen.net/groupserver/gs.group.messages.add.base>
.. [#form] See ``gs.form`` 
            <https://source.iopen.net/groupserver/gs.form/summary>
.. [#auth] See ``gs.auth.token`` 
            <https://source.iopen.net/groupserver/gs.auth.token/summary>
.. [#config] See ``gs.config`` 
            <https://source.iopen.net/groupserver/gs.config/summary>
.. _GroupServer: http://groupserver.org/
.. _Mailman: http://www.gnu.org/software/mailman/
.. _smtp2gs: https://source.iopen.net/groupserver/gs.group.messages.add.smtp2gs

..  LocalWords:  CONFIG config SMTP DebuggingServer buildout ini
..  LocalWords:  Buildlout localhost sudo
