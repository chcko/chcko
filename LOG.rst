===
LOG
===

TODO
====

Update dd,df,dc,cz and move to doc/readme

hlp.logger

https://cloud.google.com/appengine/docs/standard/python3/testing-and-deploying-your-app

20191230
========

chcko/test/test_integration.py

20191229
========

chcko/test/test_integration.py

20191228
========

chcko/test/test_integration.py

20191227
========

chcko/test/test_integration.py

Using
https://github.com/chcko/boddle
for testing.

20191226
========

chcko/test/test_sql.py
chcko/test/test_ndb.py

20191225
========

sql.py db backend implementation using sqlalchemy, parallel to ndb.py.
Next: testing sql.py and ndb.py

20191220
========

Experimenting with sqlalchemy backend implementation.
How to do the Key?

20191219
========

Created ndb.py and sql.py.
Separated all google.cloud.ndb interaction into ndb.py.
ndb.Ndb is plugged in in main.py.
sql.Sql should be plugged in the same way.
Next:

- fix and test changes
- implement sql.Sql


20191218
========

Fixing the conversion to bottle: Currently stuck with a db problem.
Since I want to support more DB backends, I will

- define a DB interface
- moving current google-cloud-ndb code to it

20191217
========

webapp2 to bottle conversion
check out bottle_session

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


20191214
========

https://github.com/GoogleCloudPlatform/python-docs-samples/tree/master/appengine/standard/ndb

Try to make *chcko* run with Python3 with minimal change,
before actually endeavor into replacing dependencies

- drop webapp2 3.0.0b1 for bottle
- drop simpleauth (for bottle-oauthlib?)
- drop ndb for own db abstraction supporting fireo and sqlalchemy

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


20191213
========

Allow more DB backends:
pdt/A/p.rst
pdt/A/d.rst
pdt/A/t.rst

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


