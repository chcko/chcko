===
LOG
===

TODO
====

Update dd,df,dc,cz and move to doc/readme

hlp.logger

20191203
========

https://github.com/mamchecker/mamchecker
is built on Python2 because Google was late to adopt Python3.

Now *google appengine* has become *google cloud platform* and Python3 is supported.
Moreover 3rd party libraries don't need to be part of the app tree.
The app tree can rather be seen as Python3 package and 3rd party libraries
listed in ``requirements.txt`` will be installed automatically.

This necessitates changes almost equivalent to a rewrite.

I Made a *new organization* to hold the python 3 version of mamchecker:
https://github.com/chcko.
Due to limited time, it will take possibly a year to complete the changes.
Luckily Goople continues to support Python2 apps.
So mamchecker stays online.
Content can be added to mamchecker.
I can be moved to chcko when chcko is completed.

Googling:

  https://github.com/GoogleCloudPlatform/appengine-bottle-skeleton
  https://github.com/GoogleCloudPlatform/appengine-photoalbum-example
  https://realpython.com/testing-third-party-apis-with-mocks/
  https://cloud.google.com/appengine/docs/standard/python3/building-app/authenticating-users
  https://github.com/Refinitiv/bottle-oauthlib/blob/master/tests/examples/quickstart_resourceserver.py
  https://github.com/Refinitiv/bottle-oauthlib/blob/master/tests/examples/quickstart_resourceserver.py
  https://googleapis.dev/python/google-api-core/latest/auth.html
  https://hackersandslackers.com/flask-login-user-authentication/
  https://github.com/devries/bottle-session
  https://github.com/GoogleCloudPlatform/flask-talisman
  https://cloud.google.com/appengine/docs/standard/python3/testing-and-deploying-your-app

20191213
========

Sifting through docs about firebase, datastore and similar software:

    https://cloud.google.com/community/tutorials/building-flask-api-with-cloud-firestore-and-deploying-to-cloud-run

    https://en.wikipedia.org/wiki/Firebase:
    Firebase is a mobile and web application development platform developed by Firebase, Inc. in 2011, then acquired by Google in 2014 ...
    In October 2017, Firebase launched Cloud Firestore, a realtime document database as the successor product to the original Firebase Realtime Database.[18][19][20][21]

    https://firebase.google.com/
    Firebase is a company name.
    FireStore is part of the Firebase products.

    Is there a *FireStore* backend for SQLAchemy?
    NO.
    https://github.com/newpro/firebase-alchemy is not for *firestore*.
    It is based on https://github.com/ozgur/python-firebase.
    It is from 2014.
    At that time Firebase had the Firebase RealTime Database.

    https://firebase.google.com/docs/firestore/quickstart
    https://firebase.google.com/docs/firestore/query-data/queries
    https://firebase.google.com/docs/rules/unit-tests

    https://firebase.google.com/docs/functions/local-emulator

    ::

      npm install -g firebase-tools
      export GOOGLE_APPLICATION_CREDENTIALS="path/to/key.json"
      firebase emulators:start

    Or https://cloud.google.com/sdk/gcloud/reference/beta/emulators/firestore/

    ::

      gcloud components install cloud-firestore-emulator beta
      gcloud beta emulators firestore start

    Alternative to using *FireStore*: Cloud SQL.
    https://cloud.google.com/sql/docs/mysql/connect-app-engine
    Could SQL works with SQLAlchemy.
    BUT: Cloud SQL has no free quota.
    Pricing:
    https://cloud.google.com/firestore/pricing
    https://cloud.google.com/sql/pricing

    https://wiki.christophchamp.com/index.php?title=Google_Cloud_Platform

    Checking the current model::

      export CLOUDSDK_CORE_PROJECT=chcko
      gcloud beta emulators datastore start

    Adding ``with db.context():`` according
    https://github.com/googleapis/python-ndb/blob/master/docs/migrating.rst


Plan: DB abstraction
--------------------

*Mamchecker* depended on Google *DataStore*, via *ndb*.

Now *ndb* and *DataStore* are also supported for Python 3.
Google rebranded *DataStore* to *FireStore* after buying the *FireBase* company.
*Datastore* is still available as a compatibility mode to *FireStore*.
https://stackoverflow.com/questions/47689003/google-firestore-a-subset-or-superset-of-google-cloud-datastore.

- *FireStore* (and *DataStore*) are addressed via

  - REST api (POST and GET json to HTTP addresses)
  - GRPC api (proto3 protobuf

  But there are client libraries.
  For Python the official one is https://pypi.org/project/google-cloud-firestore.
  There is also
  https://pypi.org/project/fireo/ which builds on
  https://pypi.org/project/google-cloud-firestore.

- *Relational databases* use SQL.

  Python client ORM libraries are SQLAlchemy and PonyORM.

To use both, **chcko** needs and abstraction layer.
Then it is better to build on *FireStore* directly,
instead of *DataStore*.
Other DBs can be supported with SQLAlchemy:
https://docs.sqlalchemy.org/en/13/orm/tutorial.html

Create glue code that can use

- SQLAlchemy and
- fireo

Comparing:
https://octabyte.io/FireO/quick-start/
https://docs.sqlalchemy.org/en/13/orm/tutorial.html
There are common usages/functions.

Comparing:
https://googleapis.dev/python/firestore/latest/index.html
https://docs.sqlalchemy.org/en/13/orm/tutorial.html
Fireo brings google-cloud-firestore closer to SQLAlchemy.

20191214
========

https://github.com/GoogleCloudPlatform/python-docs-samples/tree/master/appengine/standard/ndb

Make *chcko* run with Python3 with minimal change

- replace webapp2 3.0.0b1 with bottle
- drop simpleauth
- own db abstraction, first supporting google-cloud-ndb and sqlalchemy

mail problem
------------

chcko/signup/__init__.py: ``from google.appengine.api import mail`` does not support Python3
``~/.local/opt/google-cloud-sdk/platform/google_appengine/google/appengine/api/mail.py``
Problem lies in ProtocolBuffer.py containing ProtocolMessage.
Solution is in **hlp.py**.
https://gaedevs.com/blog/things-to-understand-before-migrating-your-python-2-gae-app-to-python-3
No alternative in google.cloud for Python3.
But:
https://developers.google.com/gmail/api/quickstart/python
, https://github.com/gsuitedevs/python-samples/blob/master/gmail/quickstart/quickstart.py
, https://blog.mailtrap.io/send-emails-with-gmail-api/#Step_8_Send_an_email
, https://gist.github.com/WJDigby/e36203102a195797c712c6cfe5020b21
, https://developers.google.com/gmail/api/guides/sending
, https://stackabuse.com/how-to-send-emails-with-gmail-using-python/
, https://medium.com/@erdoganyesil/read-file-from-google-cloud-storage-with-python-cf1b913bd134
Created ``chcko.mail@gmail.com`` and enabled Gmail API:
chcko/credentials.json
https://cloud.google.com/appengine/docs/standard/python3/sending-messages
, https://pypi.org/project/mailgun3-python/
, https://cloud.google.com/kms/docs/secret-management#choosing_a_secret_management_solution
, https://usefulangle.com/post/51/google-refresh-token-common-questions
, https://cloud.google.com/appengine/docs/standard/python3/using-cloud-storage
, https://cloud.google.com/appengine/docs/standard/python3/migrating-to-cloud-ndb

https://cloud.google.com/appengine/docs/admin-api/access-control#permissions_and_roles

In principle mail can be done by Gmail API.
The token from quickstart can be used, because it is only me who consents.
How to upload a token into datastore?
Manually via console.cloud.google.com, then left pane: datastore.


20191216
========

Setup testing::

  gcloud config set project chcko-262117
  gcloud beta emulators datastore start
  DATASTORE_EMULATOR_HOST=localhost:8081 gunicorn main:app

In python: ``os.environ['DATASTORE_EMULATOR_HOST']='localhost:8081'`` or whatever other port.

  ``dev_appserver.py`` is python 2, but should also run a python 3 app::

    cd ~
    python2 `which dev_appserver.py` chcko

  I get::

    google.auth.exceptions.DefaultCredentialsError: Could not automatically determine credentials. Please set GOOGLE_APPLICATION_CREDENTIALS

  Which means, it is connecting the actual server.
  https://stackoverflow.com/questions/46432589/how-to-use-python-3-with-google-app-engines-local-development-server
  means that only v1 is supported by dev_appserver.py.
  Therefore: stick to ``gcloud beta emulators``.

20191217
========

webapp2 to bottle conversion
check out bottle_session

20191218
========

Fixing the conversion to bottle: Currently stuck with a db problem.
Since I want to support more DB backends, I will

- define a DB interface
- moving current google-cloud-ndb code to it

20191219
========

Created ndb.py and sql.py.
Separated all google.cloud.ndb interaction into ndb.py.
ndb.Ndb is plugged in in main.py.
sql.Sql should be plugged in the same way.
Next:

- fix and test changes
- implement sql.Sql

20191220
========

Experimenting with sqlalchemy backend implementation.
How to do the Key?

20191225
========

sql.py db backend implementation using sqlalchemy, parallel to ndb.py.
Next: testing sql.py and ndb.py

20191226
========

chcko/tests/test_sql.py
chcko/tests/test_ndb.py

20191227
========

chcko/tests/test_content.py

Using
https://github.com/chcko/boddle
for testing.

20191228
========

chcko/tests/test_content.py

20191229
========

chcko/tests/test_content.py

20191230
========

chcko/tests/test_content.py

chcko/tests/test_sql.py
chcko/tests/test_ndb.py
to 
chcko/tests/test_db.py

20191231
========

chcko/tests/test_functional.py

https://github.com/bottlepy/bottle/issues/614
https://stackoverflow.com/questions/23360666/sqlalchemy-filter-query-by-pickletype-contents

20200101
========

chcko/tests/test_functional.py
Stuck at test_forgot,
user managment in general.
But user is needed, as it holds together more roles.

Googling and Reading:

  bottle-oauthlib is for providing oauth2 not for the openID client workflow. Removing.
  Alternative: https://github.com/avelino/bottle-auth?

  https://cloud.google.com/identity-platform/docs/how-to-enable-application-for-oidc
  https://medium.com/google-cloud/authenticating-using-google-openid-connect-tokens-e7675051213b
  Example:
  https://github.com/salrashid123/google_id_token/blob/master/python/googleidtokens.py
  It uses https://github.com/googleapis/google-auth-library-python

Reorder LOG.txt to last at bottom.
Removed pdt folder.

20200102
========

User management.

In google.appengine.api.user has gone.
Do new user handling is in an appengine/gcloud independent way.

- email/password->token to verify email
  token cookie to stay logged on

- OIDC identity to log on

https://realpython.com/flask-google-login/

1. development:
   Get client credential for chcko from each provider (XXX configuration).
   Store safely locally outside project. Apply using ``environ``.
   Google: https://console.developers.google.com/apis/credentials
   During development ``export OAUTHLIB_INSECURE_TRANSPORT=1``
2. authorization: [login with XXX] -> XXX (asks user) -> returns id token -> chcko stores id token
3. login: get access token from XXX with id token --> user info on XXX with access token

20200103
========

Comparing:

/mnt/src/google-auth-library-python: google specific
/mnt/src/loginpass: best solution
/mnt/src/bottle-auth: too old, still uses dropped bottle.ext in the example
/mnt/src/bottle-login: has its own session object, but I use /mnt/src/bottle-session already
/mnt/src/bottle-cork: more than I need
/mnt/src/bottle-authenticate: basic authentication as it is currently done, but cookie with username instead of token
/mnt/src/bottle-jwt: oidc server jwt response covered by loginpass
/mnt/src/flask-login: ok as a reference
/mnt/src/flask-oidc

User management summary:
A user is identified by a token.
The token is stored in a session.
The session is found by session cookie.
The token can result
- from a direct login
- or from OIDC.

For OIDC ``loginpass`` is currently the best google-independent solution.

20200104
========

Continuing with tests:
chcko/tests/test_functional.py
Remove bottle-session, as User is session memory.

20200105
========

chcko/tests/test_functional.py

20200106
========

chcko/tests/test_functional.py

Success on::

  py.test test/test_functional.py --db=sql


20200107
========

chcko/tests/test_functional.py::

  py.test test/test_functional.py --db=ndb

20200108
========

chcko/tests/test_functional.py

Stuck with ndb.BooleanProperty(repeated=True) stored as [None] instead of [False].

20200109
========

chcko/tests/test_functional.py::

  fixes for
  py.test test/test_functional.py --db=ndb
  conflict with --db=sql

20200110
========

make datastore emulator faster with --no-store-on-disik::

  gcloud beta emulators datastore start --no-store-on-disk

Checking profiling ndb::

  pip install --user pytest-profiling
  py.test test/test_content.py --db=ndb --profile
  pip install --user tuna
  tuna prof/*.prof

Checking ``python-ndb`` tests::

  pip install --user nox
  nox
  #only unit tests were run
  #
  #change noxfile.py 3.7 to 3.8
  export GOOGLE_CLOUD_PROJECT="chcko-262117"
  export GOOGLE_APPLICATION_CREDENTIALS="/home/roland/.config/gcloud/legacy_credentials/dontbite71@gmail.com/adc.json"
  nox -s system
  #now also system tests, but some failed due to index

``python-ndb`` is tested with the remote datastore,
unless a local emulator is started and::

  DATASTORE_EMULATOR_HOST=localhost:8081 nox -s system

20200111
========

The occasional failures of tests with ``--db=ndb``
are because ndb is only eventually consistent.
Need to use ``ndb.transaction`` in some places.

20200113
========

Use
/mnt/src/python-ndb/test_utils/test_utils/scripts/run_emulator.py

noxfile.py
setup.py

Test succeed with nox::

  nox

20200114
========

Visually check and fix the HTML layout::

  sudo pip install -e .
  chcko

20200115
========

Why does changing lang change the cookie?
Bottle cookie defaults to current path. Use path='/'.

Where is the .../null GET request coming from?
https://stackoverflow.com/questions/59755918/refreshing-the-browser-produces-a-wsgi-null-as-last-get-request-why-the-nul

20200119
========

More fixes.

