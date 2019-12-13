################
More DB Backends
################

****
Plan
****

.. _`pa0`:
:pa0: DB abstraction

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


