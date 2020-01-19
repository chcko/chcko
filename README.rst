chcko
=====

Small content items, identified with short names:

- Explanations
- Exercises with randomly generated values.

Pages:

- ``content`` page: items composed via URL
- ``contexts`` of one user
- ``done``: done exercises filtered by context
- ``todo``: assigned exercises
- some additional helper pages

Architecture:

- Server: Python 3 on GCP
- Client: HTML, Javascript (jquery, ...)

Status
------

Work in Progress.
LOG.rst.

Plan
----

Re-implement the existing HTTP interface of Mamchecker with the GCP Python 3 API:
CHANGELOG.rst

Stick to bottle and SimpleTemplate.
SimpleTemplate is just pure Python, with almost no code overhead.
SimpleTemplate's are run on the server just like other Python code.
Flask, on the other hand, would pull in Jinja2, Werkzeug, click and itsdangerous,
which are not needed.


Current Implementation
======================

The URI API is currently implemented in Python2:
`MamChecker <https://github.com/mamchecker/mamchecker>`__.

Mamchecker is available at

- `appspot <http://mamchecker.appspot.com>`_ 

Content is developed on Github.
`Mamchecker <https://github.com/mamchecker/mamchecker>`_ content format stays valid.

There is also the `Mamchecker Mailing List <https://groups.google.com/d/forum/mamchecker>`_.

For further details:
`purpose <https://github.com/mamchecker/mamchecker/blob/master/mamchecker/r/cz/en.rst>`__
`ideas <https://github.com/mamchecker/mamchecker/blob/master/mamchecker/r/da/en.rst>`__
`queries <https://github.com/mamchecker/mamchecker/blob/master/mamchecker/r/db/en.rst>`__
`query rights <https://github.com/mamchecker/mamchecker/blob/master/mamchecker/r/de/en.rst>`__
`participate <https://github.com/mamchecker/mamchecker/blob/master/mamchecker/r/dc/en.rst>`__
`history <https://github.com/mamchecker/mamchecker/blob/master/mamchecker/r/df/en.rst>`__
`try in class <https://github.com/mamchecker/mamchecker/blob/master/mamchecker/r/dd/en.rst>`__


.. mamchecker/r/cz/en.rst
   mamchecker/r/da/en.rst
   mamchecker/r/db/en.rst
   mamchecker/r/de/en.rst
   mamchecker/r/dc/en.rst
   mamchecker/r/df/en.rst
   mamchecker/r/dd/en.rst


See the `r <https://github.com/mamchecker/mamchecker/blob/master/mamchecker/r>`_ folder.
for sample content.

Generally, every author has a folder with subfolders per exercise.
The exercise folder has the exercise in several language files (templates), either as ``.html`` or as ``.rst``.
``.rst`` files are translated to html with ``dodo -kd. html``.

The data model is::

  school 1-n period 1-n teacher 1-n class 1-n student

This is called a context. A user has more contexts.

The URL format is::

  URL = "http://"domain"/"lang"/"page_request
  domain = "mamchecker.appspot.com"|"www.mamchecker.eu"
  lang = "en"|"de"|...
  page_request = ["content?"]{author"."exercise["="count]"&"}
               | "done?"context{field("~"|"="|"!"|"<"|">")value","}
               | "todo"
               | "edits?"("new"|"change"|"delete")
               | "contexts"
  context = [[[[[school&]period&]teacher&]class&]student&]

Commands
========

`dev_appserver <https://cloud.google.com/appengine/docs/python/tools/devserver>`_, 
is part of the
`appengine SDK <https://cloud.google.com/appengine/downloads>`_.
It is Python 2 but also Python 3 apps can be run locally with it.

Install Google Cloud SDK::

  cd ~/.local/opt/
  curl -OLs https://dl.google.com/dl/cloudsdk/channels/rapid/downloads/google-cloud-sdk-274.0.0-linux-x86_64.tar.gz
  tar -xf google-cloud-sdk-274.0.0-linux-x86_64.tar.gz
  rm google-cloud-sdk-274.0.0-linux-x86_64.tar.gz
  cd google-cloud-sdk
  ./install.sh

  #new terminal
  gcloud components install app-engine-python app-engine-python-extras cloud-datastore-emulator cloud-firestore-emulator beta
  #link with google account
  gcloud init --console-only
  #gcloud projects delete <sample-project-id>

Clone and initialize ``chcko``::

  cd ~
  git clone https://github.com/chcko/chcko
  cd ~/chcko/chcko
  pip install --user doit
  doit -kd. html
  cd ..
  doit initdb

Create a virtual environment::

  [ -e ~/tmp/venvchcko ] || python3 -m venv ~/tmp/venvchcko
  source ~/tmp/venvchcko/bin/activate
  cd ~/chcko
  pip install -r requirements.txt
  deactivate

Only run datastore emulator::

  #gcloud config set project chcko-262117
  pip install --user -r requirements.txt
  gcloud beta emulators datastore start
  DATASTORE_EMULATOR_HOST=localhost:8081 gunicorn main:app

Test ``chcko``::

  doit test
  doit cov
  doit serve

  #or e.g.
  #breakpoint() in code
  py.test tests/test_functional.py --db=sql
  b chcko/app.py:90
  c

Upload::

  cd ~/chcko
  gcloud app deploy app.yaml


``gcloud`` commands (see `reference <https://cloud.google.com/sdk/gcloud/reference/>`__)::

  gcloud help
  gcloud info --format yaml
  gcloud auth {list,login,revoke}
  gcloud config {list,set {account,project},configurations list}
  gcloud components {list,install,update,remove}
  gcloud app {browse,deploy,describe,deploy,open-console}


``gcloud app open-console`` opens the GCP console in the browser.

