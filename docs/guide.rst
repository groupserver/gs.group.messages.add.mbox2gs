How to import ``mbox`` files into GroupServer
=============================================

The following describes all steps before ``mbox2gs`` can be
called. This document is intended for advanced users only. **Do
not** attempt to use this unless you are really sure you know
what you are doing! You have been warned.


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

         :Important: You may want to disable SMTP in your
                     GroupServer instance while you are testing,
                     or even migrating archivesd from old Mailman
                     mailin-lists, because every email you import
                     would be send to your mailing list members.
                     Which is something you may not want to do.

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
