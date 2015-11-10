How to import ``mbox`` files into GroupServer
=============================================

.. highlight:: console

The following describes all steps before :command:`mbox2gs` can
be called. This document is intended for advanced users
only. **Only** attempt to use this if you are really sure you
know what you are doing! You have been warned.


1. **(Optional)** Disable SMTP (sending emails) in your
   GroupServer instance. You can disable SMTP in one of two ways.

   i. Modify :file:`etc/gsconfig.ini` in your GroupServer
      installation

      - In :file:`etc/gsconfig.ini` you have sections
        ``[config-default]``, which has set ``smtp = on`` by
        default. Set ``smtp = off``.

      - Stop and start again your instance so the configuration
        change takes effect.

      - Test sending of email via your GroupServer instance. No
        message should be sent.

   ii. Re-configure your GroupServer instance to use Python's
       native SMTP daemon running in debug mode:

       - SMPT port set to 2525 in :file:`config.cfg`

       - Run :program:`Buildlout`::

          $ buildout -N

       - Start the server::

          $ sudo python -m smtpd -n -c DebuggingServer localhost:2525

       - Test sending of email via your GroupServer instance. No
         message should be sent, but you should see the email in
         the DebuggingServer that you are running.

         :Important: You may want to disable SMTP in your
                     GroupServer instance while you are testing,
                     or even migrating archivesd from old
                     :program:`Mailman` mailing-lists, because
                     every email you import would be send to your
                     mailing list members.  Which is something
                     you may wish to avoid.

2. Prepare :program:`Mailman` archives for migration.

   Long story short, things are not in ideal shape in any
   :program:`Mailman` archive out there, because:

   - Email addresses are usually obfuscated (eg. *some.email at
     example.com*, *some.email*).

   - A typical :program:`Mailman` archive (usually gzipped) is
     often an invalid mbox file.

   The ``mailman2mbox`` Python script deals with the issues and
   helps you to convert your :program:`Mailman` archives to mbox
   format <https://gist.github.com/corydolphin/1728592>.

3. Create a new GroupServer group to which you intend to import
   mbox archive(s) in to.

   Example: ``http://groups.example.com/groups/my-group/``

4. Get a list of all email addresses from your Mailman
   mailing-list, or extract the list from mbox archives.

5. Load all email addresses to the group via the :guilabel:`Add
   members in bulk` page, linked from the :guilabel:`Admin`
   section of the group.

   :Note: Unless you disable SMTP everyone on the list will get
          an email about the fact that you added them to the
          group.

6. All prepared. You are now ready to migrate your ``mbox``
   archive(s) using :command:`mbox2gs` (see :doc:`script`).
