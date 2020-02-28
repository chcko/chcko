=========
CHANGELOG
=========

TODO
====

- math display improvements

- CSS use http://getbem.com/naming/

- HTML modernize, dri

- Add man file

- rework meta content

- ``pip freeze``

- Reach near 100% test coverage.
  Fix ndb tests: Currently ndb tests sometimes fail,
  most likely due to the eventually consistent nature of ndb.

0.1.4
=====

- Courses via URL

0.1.3
=====

- OAUTH login with google and facebook
- Fixes for GCLOUD

0.1.1
=====

- Adapt to changes in used 3rd party packages:
  ``google-cloud-ndb``, ``simpleauth`` dropped for ``loginpass``,
  ``webapp2`` dropped for ``bottle``.

- Allow more DB backends: done via ``SqlAlchemy`` in addition to ``google-cloud-ndb``

- Allow adding content via adding ``chcko-<author>`` packages to ``requirements.txt``

- make ``chcko`` and ``chcko-r`` Python Package


Mamchecker
==========

History as mamchecker:

- 2013-01-01: first plans.
  How to get feedback from a class of pupils in parallel?
  Found GAE.
  Subsequently first implementation and trials in class.
- 2013-08-09:
  Refactored language handling.
- 2014-03-16:
  Cleanup.
  Drop git history.
  Upload to github.
  Busy with new job, only very occasionally additional exercises.
