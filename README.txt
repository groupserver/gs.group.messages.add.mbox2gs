Introduction
============

This is the code for the `mbox2gs`_ script, which allows to import email messages
from mbox archives to `GroupServer`_.

It can be used for migration of `Mailman` mailing-list archives ie. to migrate old
mailing-lists from `Mailman` to `Groupserver`_.

This document is intended for advanced users only. DO NOT attempt to use this unless 
you are really sure you know what you are doing! You have been warned.


Before You Start
================

The following describes all steps before ``mbox2gs`` can be called.


1. (OPTIONAL) How-to Disable SMTP (sending emails) in your `GroupServer`_ instance.

   You can disable SMTP by:

   a) Modifying /path/to/your/instance/parts/instance/etc/gsconfig.ini

      - In `gsconfig.ini` you have sections `[config-default]` which has set `smtp = on` by default. Set `smtp = off`.
      - Stop and start again your instance so the configuration change takes effect.
      - Test sending of email via your `GroupServer` instance. You should not get any.

   b) Re-configure your `GroupServer`_ instance to use Python's native SMTP daemon running in debug mode:
      - SMPT port set to 2525 in `config.cfg` 
      - Run `buildout -N`
      - Run `sudo python -m smtpd -n -c DebuggingServer localhost:2525`
      - Test sending of email via your `GroupServer` instance. You should not get any and you should see the email
        appearing in the DebuggingServer that you are running.

IMPORTANT: You may want to disable SMTP in your `GroupServer` instance while you are testing, or even migrating
archivesd from old Mailman mailin-lists, because every email you import would be send to your mailing list members.
Which is something you may not want to do.


2. Prepare Mailman archives for migration.

   Long story short, things are not in ideal shape in any `Mailman`_ archive out there, because:

   - Email addresses are usually obfuscated (eg. *some.email at example.com*, *some.email*).
   - Typical `Mailman`_ archive (usually gzipped) is not a proper mbox file.

   The following Python script deals with the issues and helps you to convert your `Mailman`_ archives to mbox format.

   https://gist.github.com/wcdolphin/1728592


3. Create a new `GroupServer`_ group to which you intend to import mbox archive(s) in to.

   Example: http://example.org/groups/my-group/


4. Get a list of all email addresses from your `Mailman`_ mailing-list, or extract the list from mbox archives. 

   Note, that everyone on the list will get an email about the fact that you added them to the group.


5. Load all email addresses to the group via `admin_join_add_csv.html` page.

   Example: http://example.org/groups/my-group/admin_join_add_csv.html

6. All prepared. You are now ready to migrate your mbox archive(s) using ``mbox2gs``.


``mbox2gs``
===========

Usually an advanced user of Groupserver calls ``mbox2gs`` when required to add 
email messages from mbox archive to a GroupServer group. 

``mbox2gs`` is defined as an entry point [#entryPoint]_ to this module.


Usage
-----

::

   mbox2gs [-h] [-m MAXSIZE] [-l LISTID] [-f FILE] [-c CONFIG] [-i INSTANCE] url

Positional Arguments
~~~~~~~~~~~~~~~~~~~~

``url``:
  The URL for the GroupServer site.

``-l LISTID``, ``--list LISTID``:
  The list to send the message to. By default it is extracted from the 
  ``x-original-to`` header. If your mbox archive contains ``x-original-to`` 
  then your group/list id MUST be the same as ``x-original-to``. 

``-f FILE``, ``--file FILE``:
  The name of the file that contains the mbox archive. Only one archive
  can be imported at the time.

Optional Arguments
~~~~~~~~~~~~~~~~~~

``-h``, ``--help``:
  Show a help message and exit

``-m MAXSIZE``, ``--max-size MAXSIZE``:
  The maximum size of the post that will be accepted, in mebibytes (default 
  200MiB).

``-c CONFIG``, ``--config CONFIG``:
  The name of the GroupServer `configuration file`_ (default
  "$INSTANCE_HOME/etc/gsconfig.ini") that contains the token that will be
  used to authenticate the script when it tries to add the email to the
  site.

``-i INSTANCE``, ``--instance INSTANCE``:
  The identifier of the GroupServer instance configuration to use (default
  "default").

Returns
-------

The script returns ``0`` on success, an non-zero on an error. In the case
of an error, ``mbox2gs`` follows the convention specified in
``/usr/include/sysexits.h``. In addition the error message that is written
to ``stderr`` starts with the enhanced mail system status code
[#rfc3463]_. These include `transient errors`_ and `permanent errors`_.

Transient Errors
~~~~~~~~~~~~~~~~

Any errors that can be solved by changing the configuration (either of
Postfix or the `configuration file`_) are marked as *transient* (with a
``4.x.x`` status code). 

======  ===================================  ==================================
 Code    Note                                 Fix
======  ===================================  ==================================
 4.3.5   Error with the configuration file.   Correct the configuration file.
 4.4.4   Error connecting to URL.             Check that the server is running, 
                                              or alter the URL that is used to 
                                              call ``mbox2gs``.
 4.4.5   The system is too busy.              Wait.
 4.5.0   Could not decode the data            *Usually* this is caused by an
         returned by the server.              invalid token in the 
                                              `configuration file`_.
                                              Fix the token in the file.
 4.5.2   No host in the URL.                  Alter the URL that is used in 
                                              the call to ``mbox2gs`` so it has
                                              a host-name.
======  ===================================  ==================================


Permanent Errors
~~~~~~~~~~~~~~~~

The five *permanent* errors are listed below.

======  ======================================================================
 Code    Note
======  ======================================================================
 5.1.1   There is no such group to send the message to.
 5.1.3   No "x-original-to" header in the email message.
 5.3.0   The file containing the email was empty.
 5.3.4   Email message too large.
 5.5.0   Error communicating with the server (either while looking up the
         group information or adding the message).
======  ======================================================================


Examples
--------

Importing a mbox archive to a group in the general case::

  mbox2gs --list newGroupId --file /tmp/test.mbox http://url.of.your.site


The Code
--------

The ``mbox2gs`` script is provided by the module
``gs.group.messages.add.mbox2gs.script``. The ``main`` function takes the
name of the default configuration file a single argument, which is normally
supplied by ``buildout`` when it generates the ``mbox2gs`` script from the
entry point.

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

.. [#entryPoint] See `Feature 3539 <https://redmine.iopen.net/issues/3539>`_
.. [#rfc3463] `RFC 3463: Enhanced Mail System Status Codes 
             <http://tools.ietf.org/html/rfc3463>`_
.. [#add] See ``gs.group.messages.add.base`` 
            <https://source.iopen.net/groupserver/gs.group.messages.add.base/summary>
.. [#form] See ``gs.form`` 
            <https://source.iopen.net/groupserver/gs.form/summary>
.. [#auth] See ``gs.auth.token`` 
            <https://source.iopen.net/groupserver/gs.auth.token/summary>
.. [#config] See ``gs.config`` 
            <https://source.iopen.net/groupserver/gs.config/summary>
.. _GroupServer: http://groupserver.org/
.. _Mailman: http://www.gnu.org/software/mailman/

..  LocalWords:  CONFIG config
