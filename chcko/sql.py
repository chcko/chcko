#def python_path():
#    d = os.path.dirname
#    local_dir = d(d(__file__))
#    if local_dir not in sys.path:
#        sys.path.insert(0, local_dir)
#python_path()

import datetime
from time import monotonic_ns
import base64
from itertools import chain

from chcko.hlp import normqs, db_mixin
import chcko.auth as auth

import threading

from sqlalchemy.ext.declarative import as_declarative
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.ext.declarative.api import declared_attr
from sqlalchemy import *
C = Column

from sqlalchemy import create_engine
from sqlalchemy import util
from sqlalchemy.orm import scoped_session, sessionmaker

engine = create_engine("sqlite://")
meta = MetaData(engine)

DBSession = scoped_session(sessionmaker(bind=engine))

class Context:
    def __init__(self):
        self.dbsession = DBSession()
    def __enter__(self):
        return self.dbsession
    def __exit__(self, type_, value, traceback):
        try:
            self.dbsession.commit()
        except:
            with util.safe_reraise():
                self.dbsession.rollback()
        else:
            self.dbsession.rollback()
        DBSession.remove()

class Client:
    def context(self):
        return Context()

#pad64=lambda x: x+b"="*((4-len(x)%4)%4)
pad64=lambda x: x+b"="*3
class Key:
    '''A key is like a word in the sense that it is an address to the entity.
    It has more views, though

    used::

        __init__(urlsafe='uvw') __init__(Model1,ID1, Model2,ID2,...)
        pairs() string_id() urlsafe() kind() parent() get() delete() 

    not used::

        id() integer_id()
    '''

    def __init__(self,*args,**kwargs):#Class[name],id,...,[parent=key]
        urlsafe = kwargs.pop('urlsafe',None)
        if urlsafe is not None:
            if isinstance(urlsafe,str):
                urlsafe = urlsafe.encode()
            args = base64.urlsafe_b64decode(pad64(urlsafe)).decode().split(',')
        tblname = lambda x: isinstance(x,str) and x or x.__tablename__
        self.strpth = tuple((tblname(args[2*i]),args[2*i+1]) for i in range(len(args)//2))
        parnt = kwargs.pop('parent',None)
        if parnt:
            self.strpth = parnt.pairs()+self.strpth
        self.pth = [(_cls[k],v) for k,v in self.strpth]
    def __eq__(self, other):
        return self.strpth == other.strpth
    def _query(self):
        thscls = self.pth[-1][0]
        return DBSession().query(thscls).filter(thscls.urlkey==self.urlsafe())
    def get(self):
        return self._query().first()
    def delete(self):
        try:
            self._query().delete()
        except:
            pass
    def string_id(self):
        return self.pth[-1][1]
    def pairs(self):
        return self.strpth
    def flat(self):
        return list(chain(*self.strpth))
    def urlsafe(self):
        flt = ','.join(self.flat())
        res = base64.urlsafe_b64encode(flt.encode()).strip(b'=').decode()
        return res
    def kind(self):
        return self.pth[-1][0].__tablename__
    def parent(self):
        flt = self.flat()
        parentflat = flt[:-2]
        return parentflat and Key(*parentflat) or None

class _Counter(object):
    def __init__(self, value=0):
        self.val = value
        self.lock = threading.Lock()
    def __call__(self):
        with self.lock:
            self.val += 1
            return str(self.val)

@as_declarative(metadata=meta)
class Model(object):
    def put(self):
        DBSession().add(self)
    @property
    def key(self):
        thiskey = Key(urlsafe=self.urlkey)
        return thiskey
    @property
    def parent(self):
        return Key(urlsafe=self.urlkey).parent()
    @declared_attr
    def __tablename__(cls):
        return cls.__name__
    @declared_attr
    def __table_args__(cls):
        return {'extend_existing':True}
    _cols={}
    @classmethod
    def cols(cls):
        clsname = cls.__name__
        if clsname not in cls._cols:
            cls._cols[clsname] = [x['name'] for x in _inspect.get_columns(clsname)]
        return cls._cols[clsname]
    _cntr={}
    @classmethod
    def cnt_next(cls):
        if cls.__name__ not in cls._cntr:
            cls._cntr[cls.__name__] = _Counter(monotonic_ns())
        return cls._cntr[cls.__name__]()
    urlkey=C(String,primary_key=True,autoincrement=False)
    id=C(String)
    @classmethod
    def create(cls,*args,**kwargs):
        clsname = cls.__name__
        id = None
        if len(args) > 0:
            id = args[0]
        else:
            id = kwargs.pop('id',None)
        if id is None:
            id = str(cls.cnt_next())
        parent=kwargs.pop('parent',None)
        if parent:
            kwargs['ofkey'] = parent.urlsafe()
        thiskey = kwargs.pop('key',None)
        if thiskey is None:
            thiskey = Key(clsname,id,parent=parent)
        urlkey = isinstance(thiskey,str) and thiskey or thiskey.urlsafe()
        cols = cls.cols()
        rec = {s: kwargs[s] for s in cols if s in kwargs}
        rec.update(dict(id=thiskey.string_id(),urlkey=urlkey))
        return cls(**rec)
    @classmethod
    def get_or_insert(cls,name,*args,**kwargs):
        acls = cls.create(id=name,*args,**kwargs)
        dbsession = DBSession()
        found = dbsession.query(cls).filter(cls.urlkey==acls.urlkey).first()
        if found:
            return found
        dbsession.begin_nested()
        try:
            dbsession.add(acls)
            dbsession.commit()
        except IntegrityError as e:
            dbsession.rollback()
            acls = dbsession.query(cls).filter(cls.urlkey==acls.urlkey).one()
        return acls

class UserToken(Model):
    email = C(String)
    created = C(DateTime,default=datetime.datetime.now)
    updated = C(DateTime,default=datetime.datetime.now)
class User(Model):
    fullname = C(String)
    pwhash = C(String)
    token_model = C(ForeignKey('UserToken.urlkey'))
    current_student = C(ForeignKey('Student.urlkey',use_alter=True))
class Secret(Model):
    secret = C(String)

class School(Model):
    userkey = C(ForeignKey('User.urlkey'))
    created = C(DateTime,default=datetime.datetime.now)
class Period(Model):
    userkey = C(ForeignKey('User.urlkey'))
    created = C(DateTime,default=datetime.datetime.now)
    ofkey = C(ForeignKey('School.urlkey'))
class Teacher(Model):
    userkey = C(ForeignKey('User.urlkey'))
    created = C(DateTime,default=datetime.datetime.now)
    ofkey = C(ForeignKey('Period.urlkey'))
class Class(Model):
    userkey = C(ForeignKey('User.urlkey'))
    created = C(DateTime,default=datetime.datetime.now)
    ofkey = C(ForeignKey('Teacher.urlkey'))
class Student(Model):
    userkey = C(ForeignKey('User.urlkey'))
    created = C(DateTime,default=datetime.datetime.now)
    ofkey = C(ForeignKey('Class.urlkey'))
    color = C(String)
class Problem(Model):
    userkey = C(ForeignKey('User.urlkey'))
    ofkey = C(ForeignKey('Student.urlkey'))
    query_string = C(String)
    lang = C(String)
    # the numbers randomly chosen, in python dict format
    given = C(PickleType)
    created = C(DateTime,default=datetime.datetime.now)
    answered = C(DateTime)
    # links to a collection: 1-n, p.problem_set.get()!
    collection = C(ForeignKey('Problem.urlkey'))


    # a list of names given to the questions (e.g '1','2')
    inputids = C(PickleType)#C(ARRAY(String))
    # calculated from given, then standard formatted to strings
    results = C(PickleType)#C(ARRAY(String))
    oks = C(PickleType)#C(ARRAY(Boolean))
    points = C(PickleType)#C(ARRAY(Integer))
    # standard formatted from input
    answers = C(PickleType)#C(ARRAY(String))
    nr = C(Integer)  # needed to restore order

    @hybrid_property
    def answersempty(self):
        return ''.join(self.answers)==''
    @hybrid_property
    def link(self):
        return '/' + self.lang + '/content?' + self.query_string

class Assignment(Model):
    userkey = C(ForeignKey('User.urlkey'))
    created = C(DateTime,default=datetime.datetime.now)
    ofkey = C(ForeignKey('Student.urlkey'))
    query_string = C(String)
    due = C(DateTime)

class Index(Model):
    path = C(String)
    knd = C(Integer)
    level = C(Integer)


meta.create_all()

_cls = {x.__tablename__:x for x in [School,Period,Teacher,Class,Student,Problem,Assignment,Index,UserToken,User,Secret]}
_inspect = inspect(engine)

class Sql(db_mixin):
    def __init__(self):
        self.dbclient = Client()
        self.Key = Key
        self.models = _cls
        for k,v in _cls.items():
            setattr(self,k,v)
        self.init_db()

    def is_sql(self):
        return True
    def allof(self,query):
        return query.all()
    def first(self,query):
        return query.first()
    def ofof(self,oe):
        return oe.ofkey
    def idof(self,obj):
        return obj.urlkey
    def nameof(self,entity):
        return entity.__tablename__
    def columnsof(self,entity):
        for x in _inspect.get_columns(self.nameof(entity)):
            yield x['name']
    def fieldsof(self,obj):
        return {clmnm: getattr(obj,clmnm) for clmnm in self.columnsof(obj)}
    def add_to_set(self,problem,other):
        problem.collection = other.urlkey

    def query(self,entity,filt=None,ordr=None,parent=None):
        _filt = filt or []
        q = DBSession().query(entity).filter(*((_filt+[self.ofof(entity)==parent]) if parent else _filt))
        if ordr:
            q = q.order_by(ordr)
        return q

    def delete(self,query):
        query.delete()
    def filter_expression(self,ap,op,av):
        return text(f'{ap}{op}"{av}"')

