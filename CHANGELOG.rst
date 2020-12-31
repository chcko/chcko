=========
CHANGELOG
=========

TODO
====

- Add man file

- Reach near 100% test coverage.
  Fix ndb tests: Currently ndb tests sometimes fail,
  most likely due to the eventually consistent nature of ndb.

- HTML modernize, DRY

- CSS use http://getbem.com/naming/?

1.3.1 - 20201231
================

- Add permission to list schools for site-owner.
- Check tests and adapt chcko-r to schemdraw changes

1.3.0, 20200113-20200417
========================

- rename global defines for problem templates.

- Courses via URL

- math display improvements

- find images, locally if non-installed, and on gcloud

- OAUTH login with google and facebook

- Adapt to changes in used 3rd party packages:
  ``google-cloud-ndb``, ``simpleauth`` dropped for ``loginpass``,
  ``webapp2`` dropped for ``bottle``.

- Allow more DB backends: done via ``SqlAlchemy`` in addition to ``google-cloud-ndb``

- Allow adding content via adding ``chcko-<author>`` packages to ``requirements.txt``

- make ``chcko`` and ``chcko-r`` Python Package


Mamchecker
==========

History as mamchecker:

- 20130101: first plans.
  How to get feedback from a class of pupils in parallel?
  Found GAE.
  Subsequently first implementation and trials in class.

- 20130809:
  Refactored language handling.

- 20140316:
  Cleanup.
  Drop git history.
  Upload to github.
  Busy with new job, only very occasionally additional exercises.
