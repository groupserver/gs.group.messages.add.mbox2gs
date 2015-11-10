:program:`mbox2gs`
==================

.. program:: mbox2gs

Synopsis
--------

   :program:`mbox2gs` [:option:`-h`] [:option:`-v`] [:option:`-l` <LISTID>] [:option:`-f` <FILE>] [:option:`-c` <CONFIG>] [:option:`-i` <INSTANCE>] :option:`url`

Description
-----------

Usually, an advanced user of Groupserver calls :program:`mbox2gs` when
required to add email messages from mbox archive to a GroupServer
group.

Positional Arguments
--------------------

.. option:: url

  The URL for the GroupServer site.

Optional Arguments
------------------

.. option:: -h, --help

  Show a help message and exit.

.. option:: -v, --verbose

  Turn on verbose output (default is quiet: no news is good
  news).

.. option:: -l <LISTID>, --list <LISTID>

  The list to send the message to. By default it is extracted
  from the :mailheader:`x-original-to` header.

.. option:: -f <FILE>, --file <FILE>

  The name of the file that contains the mbox archive. Only one
  archive can be imported at the time. If omitted (or ``-``)
  standard-input will be read.

.. option:: -c <CONFIG>, --config <CONFIG>

  The name of the GroupServer configuration file (default
  :file:`{INSTANCE_HOME}/etc/gsconfig.ini`) that contains the
  token that will be used to authenticate the script when it
  tries to add the email to the site. (See :doc:`config` for more
  information.)

.. option:: -i <INSTANCE>, --instance <INSTANCE>

  The identifier of the GroupServer instance configuration to use
  (default ``default``).

Returns
-------

The script returns ``0`` on success, or a non-zero on an
error. In the case of an error, :program:`mbox2gs` follows the
convention specified in :file:`/usr/include/sysexits.h`. In
addition the error message that is written to ``stderr`` starts
with the enhanced mail system status code (:rfc:`3463`). See
smtp2gs_ for more information.

Examples
--------

Import the mbox archive stored in :file:`/tmp/test.mbox` into the
group ``my_group`` that is on the site ``groups.example.com``,
and produce verbose output:

.. code-block:: console

  $ mbox2gs -v -l my_group -f /tmp/test.mbox http://groups.example.com

.. _smtp2gs:
   https://github.com/groupserver/gs.group.messages.add.smtp2gs
