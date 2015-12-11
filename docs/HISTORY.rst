Changelog
=========

2.1.3 (2015-12-11)
------------------

* Fixing the unit-tests so they work with `zc.recipe.testrunner`_

.. _zc.recipe.testrunner:
   https://pypi.python.org/pypi/zc.recipe.testrunner

2.1.2 (2015-11-10)
------------------

* Fixing the link to the ``mailman2mbox`` script, thanks to
  `Alexander Köplinger`_

.. _Alexander Köplinger: https://github.com/akoeplinger

2.1.1 (2015-05-12)
------------------

* Fixing the ``man`` page documentation

2.1.0 (2015-03-24)
------------------

* Following the changes to the relay-address prefix in
  `gs.group.messages.add.smtp2gs`_
* Moving all the documentation to the ``docs`` folder, and
  rendering them on `Read The Docs`_
* Naming all the ReStructuredText files as such
* Switching to GitHub_ as the primary code repository


.. _Read The Docs:
   http://groupserver.readthedocs.org/projects/gsgroupmessagesaddmbox2gs/
.. _GitHub:
   https://github.com/groupserver/gs.group.messages.add.mbox2gs


2.0.0 (2014-05-05)
------------------

* Adding a *verbose* flag
* Using `gs.group.messages.add.smtp2gs`_ as a module
* Adding a smoke-test with Tox

1.0.1 (2014-02-06)
------------------

* Switching to Unicode literals
* Updating the product metadata

1.0.0 (2013-03-28)
------------------

Initial version, cloned off
`gs.group.messages.add.smtp2gs`_. Prior to the creation of this
product there was some ``mbox`` importing code in
``Products.XWFMailingListManager``.

.. _gs.group.messages.add.smtp2gs:
   https://github.com/groupserver/gs.group.messages.add.smtp2gs

..  LocalWords:  Changelog smtp mbox groupserver github GitHub ReStructuredText
