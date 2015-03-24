The code
========

The ``mbox2gs`` script is provided by the module
``gs.group.messages.add.mbox2gs.script``. The ``main`` function
takes the name of the default configuration file a single
argument, which is normally supplied by ``buildout`` when it
generates the ``mbox2gs`` script from the entry point.

The script parses the command-line arguments, and calls two
further functions:

``gs.group.messages.add.smtp2gs.servercomms.get_group_info_from_address``:

  The script posts to the page
  ``/gs-group-messages-add-group-exists.html`` to check if the
  group exists, and to get some information about the group.

``gs.group.messages.add.smtp2gs.servercomms.add_post``:

  The script posts to the page
  ``/gs-group-messages-add-email.html`` to actually add the post.

Both pages are provided by the ``gs.group.messages.add.base``
module [#add]_; the data is sent by the
``gs.form.post_multipart`` function [#form]_, with
``gs.auth.token`` [#auth]_ providing authentication (see the
section Configuration File below).

.. [#add] See ``gs.group.messages.add.base`` 
            <https://github.com/groupserver/gs.group.messages.add.base>

.. [#form] See ``gs.form`` 
            <https://github.com/groupserver/gs.form/summary>

.. [#auth] See ``gs.auth.token`` 
            <https://github.com/groupserver/gs.auth.token/summary>
