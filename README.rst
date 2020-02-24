chcko
=====

Educational content server.

Content Packages
================

Content packages are separate python packages within the same ``chcko`` namespace.
An example package is https://github.com/chcko/chcko-r.
This is a technical example without didactic thread.

Content packages consist of small content items

- short explanations
- problems with randomly generated values
- courses as path through explanations and problems (TODO)

Content items are identified in the URL with ``<author_id>.<content_id>``, each short,
and correspond to the folder ``chcko/<author_id>/<content_id>/`` within the content package.
The item folder contains ``__init__.py`` and ``<language_id>.html`` files.

``<language_id>.rst`` are also possible.
They can contain `tikz <https://github.com/pgf-tikz/pgf>`__ images
and are statically converted to ``_<language_id>.html`` with::

  doit -kd. html
  doit -kd. initdb

The server can run on

- on gcloud (currently: https://mamchecker.appspot.com)
- on any other server using `sqlalchemy <https://www.sqlalchemy.org/>`__

Updating content on gcloud (TODO):

- a content package is registered in ``requirements.txt`` via pull request
- a content package author uploads a new version to https://pypi.org
- regularly a new version of chcko is deployed
  (once a day or whenever a content package has changed on pypi)


.. mamchecker/r/cz/en.rst
   mamchecker/r/da/en.rst
   mamchecker/r/db/en.rst
   mamchecker/r/de/en.rst
   mamchecker/r/dc/en.rst
   mamchecker/r/df/en.rst
   mamchecker/r/dd/en.rst


Implementation
==============

Python 3 using ``bottle``.
The code tries to stay minimal.

Database:

The data model is::

  school 1-n period 1-n teacher 1-n class 1-n student 1-n problem

The first 5 are called a context or role.
A user has more contexts.

DB for answers to problems

- on GCP using DataStore with ``ndb`` or
- on any other server using a SQL database with ``SqlAlchemy``

Templates:

- ``bottle`` SimpleTemplate

The URL format is::

  URL = "https://"domain"/"lang"/"page_request"
  domain = "mamchecker.appspot.com"
  lang = "en"|"de"|...
  page_request = ["content?"]{author"."exercise["="count]"&"}
               | "done?"context{field("~"|"="|"!"|"<"|">")value","}
               | "todo"
               | "edits?"("new"|"change"|"delete")
               | "contexts"
  context = [[[[[school&]period&]teacher&]class&]student&]

Pages:

- ``content``: overview or items composed via URL
- ``contexts``: contexts of one user
- ``done``: done exercises filtered by context
- ``todo``: assigned exercises
- some additional helper pages

Environment Variables
---------------------

:CHCKOSECRET: a secret used to encode the user token cookie
:CHCKOPORT: used to change port for local server
:SOCIAL_AUTH_<PROVIDER>_KEY: for social login
:SOCIAL_AUTH_<PROVIDER>_SECRET: for social login


.. :CHCKO_MAIL_CREDENTIAL: used for verifying email addresses
   (currently not used due to with_email_verification=False)

Commands
========

Install Google Cloud SDK::

  cd ~/.local/opt/
  curl -OLs https://dl.google.com/dl/cloudsdk/channels/rapid/downloads/google-cloud-sdk-274.0.0-linux-x86_64.tar.gz
  tar -xf google-cloud-sdk-274.0.0-linux-x86_64.tar.gz
  rm google-cloud-sdk-274.0.0-linux-x86_64.tar.gz
  cd google-cloud-sdk
  ./install.sh

  #new terminal
  gcloud components install cloud-datastore-emulator cloud-firestore-emulator beta
  #link with google account
  gcloud init --console-only
  #gcloud projects delete <sample-project-id>

Clone and initialize ``chcko``::

  cd ~/mine
  git clone https://github.com/chcko/chcko
  git clone https://github.com/chcko/chcko-r #sample content
  pip install --user doit

Pepare content::

  cd ~/mine/chcko-r/chcko/r
  doit -kd. html
  cd ~/mine/chcko-r
  doit initdb

Run based on sql without installing::

  cd ~/mine/chcko
  ./runchcko_with_sql.py

  #if OSError: [Errno 98] Address already in use
  export CHCKOPORT=8382
  ./runchcko_with_sql.py

Virtual environment::

  nox
  source .nox/test_sql/bin/activate
  deactivate

  #gcloud config set project chcko-262117
  gcloud beta emulators datastore start --no-store-on-disk

  ./runchcko_with_emulator.py


Test ``chcko``::

  # unit tests
  cd ~/mine/chcko
  make test
  make cov
  doit test
  doit cov
  nox

  # install test
  pip uninstall chcko-r
  pip uninstall chcko
  ~/mine/chcko
  pip install --user .
  ~/mine/chcko-r
  pip install --user .
  cd
  runchcko

  #breakpoint() in code
  cd chcko
  py.test chcko/chcko/tests/test_functional.py --db=sql
  b chcko/chcko/app.py:90
  c

Upload::

  cd ~/mine/chcko
  gcloud app deploy app.yaml

``gcloud`` commands (see `reference <https://cloud.google.com/sdk/gcloud/reference/>`__)::

  gcloud help
  gcloud info --format yaml
  gcloud auth {list,login,revoke}
  gcloud config {list,set {account,project},configurations list}
  gcloud components {list,install,update,remove}
  gcloud app {browse,deploy,describe,deploy,open-console}

``gcloud app open-console`` opens the GCP console in the browser.

