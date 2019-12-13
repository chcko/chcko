===
LOG
===

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

Adding ``with db.context() as context:`` according
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

