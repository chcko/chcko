from sqlalchemy.ext.declarative import as_declarative
from sqlalchemy.ext.declarative.api import declared_attr

from sqlalchemy import *
C = Column

@as_declarative()
class Model(object):
    """Use as base class for models:

    Define models in one file:

    >>> class User(Model):
    >>>     name = C(String)

    Have a separate files with the data:

    >>> def user(ID, name):
    >>>     #if ID in globals():
    >>>     #    raise ValueError("'%s' is duplicate"%ID)
    >>>     globals()[ID] = User(ID=ID,name=name)
    >>> user('user1',"user one")
    >>> user('user2',"user two")
    >>> del user

    Use the data:

    >>> user1.name
    'user one'
    >>> user2.name
    'user two'
    >>> User.metadata.tables['user'].columns
    ['user.ID', 'user.name']

    """

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()
    @declared_attr
    def __table_args__(cls):
        return {'extend_existing':True}
    ID = C(String,primary_key=True,autoincrement=False)

class Sql:
    ''' provides interface of ndb.Ndb using SqlAlchemy
    TODO
    '''
    pass
