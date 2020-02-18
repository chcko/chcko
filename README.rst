chcko
=====

Educational content server.

Content packages are separate.
Content packages consist of small content items
identified with short names.

- short explanations
- problems with randomly generated values
- courses as path through explanations and problems

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

Content
-------

Every author has a separate ``chcko-X`` package within the ``chcko`` namespace.

The exercise folder has the exercise in several language files (templates), either as ``.html`` or as ``.rst``.
``.rst`` files are translated to html with ``dodo -kd. html``.

Translations are done via pull requests.

.. mamchecker/r/cz/en.rst
   mamchecker/r/da/en.rst
   mamchecker/r/db/en.rst
   mamchecker/r/de/en.rst
   mamchecker/r/dc/en.rst
   mamchecker/r/df/en.rst
   mamchecker/r/dd/en.rst

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
  cd ~/mine/chcko/chcko/chcko
  cd ..
  doit initdb

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

