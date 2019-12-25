#def python_path():
#    d = os.path.dirname
#    local_dir = d(d(__file__))
#    if local_dir not in sys.path:
#        sys.path.insert(0, local_dir)
#python_path()

import time
from bottle import SimpleTemplate

from chcko.hlp import key_value_leaf_id, datefmt, normqs, filter_student, db_mixin
from chcko.languages import langkindnum, langnumkind, kindint
import chcko.auth as auth

import datetime
import base64
from itertools import chain

from sqlalchemy.ext.declarative import as_declarative
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.ext.declarative.api import declared_attr
#from sqlalchemy.schema import CreateColumn
#from sqlalchemy.ext.compiler import compiles
#from sqlalchemy.orm.mapper import Mapper
from sqlalchemy import *
C = Column

from sqlalchemy import create_engine
from sqlalchemy import util
from sqlalchemy.orm import scoped_session, sessionmaker

engine = create_engine("sqlite://")
meta = MetaData(engine)

DbSession = scoped_session(sessionmaker(bind=engine))

class Context:
    def __init__(self):
        self.dbsession = DbSession()
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
        DbSession.remove()

class Client:
    def context(self):
        return Context()

class Key:
    '''A key is like a word in the sense that it is an address to the entity.
    It has more views, though

    used::

        __init__(urlsafe=xxx) __init__(Model1,ID1, Model2,ID2,...)
        pairs() string_id() urlsafe() kind() parent() get() delete() 

    not used::

        id() integer_id()

    Examples from ndb::

        dbclient=ndb.Client('chcko')
        c = dbclient.context
        with c(): k=ndb.Key('UserToken',1)                                  #
        with c(): nv=k.get()                                                #
        with c(): print(nv.subject,nv.email)                                #signup email1
        with c(): print(k.pairs())                                          #(('UserToken', 1),)
        with c(): print(k.urlsafe())                                        #b'agVjaGNrb3IPCxIJVXNlclRva2VuGAEM'
        with c(): print(nv.key.pairs())                                     #(('UserToken', 1),)
        with c(): print(nv.key.kind())                                      #UserToken

    >>> k = Key('School', '1', 'Period', '1', 'Teacher', '1', 'Class', '1', 'Student', '1')
    >>> k.pairs()
    (('School', '1'), ('Period', '1'), ('Teacher', '1'), ('Class', '1'), ('Student', '1'))
    >>> k.urlsafe()
    U2Nob29sLDEsUGVyaW9kLDEsVGVhY2hlciwxLENsYXNzLDEsU3R1ZGVudCwx
    >>> k.string_id()
    1
    >>> s=School(ID="1")
    >>> s.put()
    >>> DbSession().query(School).one().ID
    >>> p=Period(ID="1",of="1")
    >>> p.put()
    >>> DbSession().query(Period).one().ID
    >>> t=Teacher(ID="1",of="1")
    >>> t.put()
    >>> DbSession().query(Teacher).one().ID
    >>> c=Class(ID="1",of="1")
    >>> c.put()
    >>> DbSession().query(Class).one().ID
    >>> st=Student(ID="1",of="1")
    >>> st.put()
    >>> DbSession().query(Student).one().ID
    >>> k=st.key
    >>> k.pairs()
    >>> k.get().ID
    1
    >>> k.kind()
    Student
    >>> k.parent().pairs()
    >>> k.parent().get().ID
    1

    '''

    def __init__(self,*args,**kwargs):#Class[name],id,...,[parent=key]
        urlsafe = kwargs.pop('urlsafe',None)
        if urlsafe is not None:
            args = base64.urlsafe_b64decode(urlsafe.encode()).decode().split(',')
        tblname = lambda x: isinstance(x,str) and x or x.__tablename__
        self.strpth = tuple((tblname(args[2*i]),args[2*i+1]) for i in range(len(args)//2))
        parnt = kwargs.pop('parent',None)
        if parnt:
            self.strpth = parnt.pairs()+self.strpth
        self.pth = [(_cls[k],v) for k,v in self.strpth]
    def _query(self):
        jn = DbSession().query(self.pth[-1][0]).filter(self.pth[-1][0].ID == self.pth[-1][1])
        for tp,qry in reversed(self.pth[:-1]):
            jn = jn.join(tp).filter(tp.ID == qry)
        return jn
    def get(self):
        try:
            res = self._query().one()
            return res
        except:
            return None
    def delete(self):
        try:
            self._query().delete()
        except:
            pass
    def string_id(self):
        return self.pth[-1][1]
    def pairs(self):
        return self.strpth
    def _flat(self):
        return list(chain(*self.strpth))
    def urlsafe(self):
        flat = ','.join(self._flat())
        res = base64.urlsafe_b64encode(flat.encode()).decode()
        return res
    def kind(self):
        return self.pth[-1][0].__tablename__
    def parent(self):
        flat = self._flat()
        return Key(*flat[:-2])


#@compiles(CreateColumn)
#def computed_column(element, compiler, **kw):
#    col = element.element
#    result = compiler.visit_create_column(element, **kw)
#    if "computed" in col.info:
#        result += " AS (%s) STORED" % col.info["computed"]
#    return result


@as_declarative(metadata=meta)
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

    def put(self):
        DbSession().add(self)
    @classmethod
    def get_or_insert(cls,*args,**kwargs):
        ID = kwargs['ID']
        found = DbSession().query(cls).filter(cls.ID == ID).first()
        if found:
            return found
        nfound = cls(*args,**kwargs)
        dbsession = DbSession()
        dbsession.begin_nested()
        try:
            dbsession.add(nfound)
            dbsession.commit()
        except IntegrityError as e:
            dbsession.rollback()
            nfound = dbsession.query(cls).filter(cls.ID == ID).one()
        return nfound
    def parent(self):
        return self.key.parent().get()
    @property
    def key(self):
        name = self.__class__.__table__.key
        mdls = list(_pthcls.keys())
        try:
            iname = mdls.index(name)
            rpth = []
            c = self
            while iname>=0:  #XXX avoid a loop
                rpth += [c.ID,school_context[iname]]
                iname = iname - 1
                if iname>=0:
                    _c = _cls[school_context[iname]]
                    c = DbSession().query(_c).filter(_c.ID==c.of).one()
            flat = list(reversed(rpth))
            res = Key(*flat)
        except:
            res = Key(name,self.ID)
        return res
    @declared_attr
    def __tablename__(cls):
        return cls.__name__
    @declared_attr
    def __table_args__(cls):
        return {'extend_existing':True}
    ID = C(String,primary_key=True,autoincrement=False)

class UserToken(Model):
    subject = C(String,nullable=False)
    token = C(String,nullable=False)
    email = C(String)
    created = C(DateTime,default=datetime.datetime.now)
    updated = C(DateTime,default=datetime.datetime.now)
    @classmethod
    def selfmadekey(cls, subject, token):
        return Key(cls, '%s.%s' % (subject, token))
    @classmethod
    def create(cls, email, subject, token=None):
        email = email
        token = token or gen_salt()
        key = cls.selfmadekey(subject, token)
        entity = cls(ID=key.string_id(), email=email, subject=subject, token=token)
        entity.put()
        return entity
class User(Model):
    pwhash = C(String)
    token_model = C(ForeignKey('UserToken.ID'))
    current_student = C(ForeignKey('Student.ID',use_alter=True))
    def set_password(self, password):
        self.pwhash = generate_password_hash(password)
    @classmethod
    def create(cls, email, password):
        user = cls.by_login(email,password)
        if not user:
            user = cls.get_or_insert(ID=email, pwhash=generate_password_hash(password))
        return user
    @classmethod
    def by_login(cls,email,password):
        user = Key(cls,email).get()
        if user:
            if not check_password_hash(user.pwhash,password):
                return None
        return user
    @hybrid_property
    def email(self):
        return self.ID
class Secret(Model):  # filled manually
    secret = C(String)


class School(Model):
    userkey = C(ForeignKey('User.ID'))
    created = C(DateTime,default=datetime.datetime.now)
class Period(Model):
    userkey = C(ForeignKey('User.ID'))
    created = C(DateTime,default=datetime.datetime.now)
    of = C(ForeignKey('School.ID'))
class Teacher(Model):
    userkey = C(ForeignKey('User.ID'))
    created = C(DateTime,default=datetime.datetime.now)
    of = C(ForeignKey('Period.ID'))
class Class(Model):
    userkey = C(ForeignKey('User.ID'))
    created = C(DateTime,default=datetime.datetime.now)
    of = C(ForeignKey('Teacher.ID'))
class Student(Model):
    userkey = C(ForeignKey('User.ID'))
    created = C(DateTime,default=datetime.datetime.now)
    of = C(ForeignKey('Class.ID'))
    color = C(String)
class Problem(Model):
    userkey = C(ForeignKey('User.ID'))
    of = C(ForeignKey('Student.ID'))
    query_string = C(String)
    lang = C(String)
    # the numbers randomly chosen, in python dict format
    given = C(PickleType)
    created = C(DateTime,default=datetime.datetime.now)
    answered = C(DateTime)
    # links to a collection: 1-n, p.problem_set.get()!
    collection = C(ForeignKey('Problem.ID'))


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
    userkey = C(ForeignKey('User.ID'))
    created = C(DateTime,default=datetime.datetime.now)
    of = C(ForeignKey('Student.ID'))
    query_string = C(String)
    due = C(DateTime)

class Index(Model):
    path = C(String)
    knd = C(Integer)
    level = C(Integer)

meta.create_all()

_cls = {x.__tablename__:x for x in [School,Period,Teacher,Class,Student,Problem,Assignment,Index,UserToken,User,Secret]}
_pthcls = {'School':School, 'Period':Period, 'Teacher':Teacher, 'Class':Class, 'Student':Student, 'Problem':Problem}
_inspect = inspect(engine)
_probcols = [x['name'] for x in _inspect.get_columns('Problem')]

#_inspect.get_table_names() #['Assignment', 'Class', 'Index', 'Period', 'Problem', 'School', 'Secret', 'Student', 'Teacher', 'User', 'UserToken']
#_inspect.get_columns('School') #[{'name': 'ID', 'type': VARCHAR(), 'nullable': False, 'default': None, 'autoincrement': 'auto', 'primary_key': 1}, {'name': 'userkey', 'type': VARCHAR(), 'nullable': True, 'default': None, 'autoincrement': 'auto', 'primary_key': 0}, {'name': 'created', 'type': DATETIME(), 'nullable': True, 'default': None, 'autoincrement': 'auto', 'primary_key': 0}]
#_inspect.get_table_names() #['Assignment', 'Class', 'Index', 'Period', 'Problem', 'School', 'Secret', 'Student', 'Teacher', 'User', 'UserToken']
#ut=UserToken() #<chcko.chcko.sql.UserToken object at 0x7ff7dc872700>
#ut.ID="1"
#ut.subject="signup"
#ut.email="email1"
#ut.token="tokn"
##UserToken.__table__.create()
#ut2=UserToken(ID='2',subject='auth',email='email2',token='tokn2')
#DbSession().add(ut)
#DbSession().add(ut2)
#DbSession().commit()
##DbSession().rollback()

#type(DbSession().query(UserToken).filter(and_(UserToken.subject=='auth',UserToken.email=='email2')).one())

#ut.subject="signup"
#ut.email="email3"
#ut.token="tokn3"
#ut.put()


class Sql(db_mixin):
    def __init__(self):
        self.dbclient = Client()
        self.Key = Key
        for k,v in _cls.items():
            set_attr(self,k,v)
        self.init_db()

    def query(self,entity,filt=None,ordr=None):
        _filt = filt or []
        q = DBSession().query(entity).filter(*_filt)
        if ordr:
            q = q.order_by(ordr)
        return q
    def delete(self,query):
        query.delete()
    def filter_expression(self,ap,op,av):
        return ap+op+av
    def problem_create(student,**pkwargs):
        return self.Problem(of=student.ID, **{s: pkwargs[s] for s in _probcols if s in pkwargs})
    def _copy_to_new_parent(self, entity, oldparent, newparent):
        self.query(entity,[self.of(entity)==self.idof(oldparent)]).update(
            {'of':newparent.ID},synchronize_session=False)
    def assign_to_student(self, studentkeyurlsafe, query_string, duedays):
        now = datetime.datetime.now()
        studentkey = self.Key(urlsafe=studentkeyurlsafe)
        Assignment(of=studentkey.string_id(), query_string=normqs(query_string),
                   due=now + datetime.timedelta(days=int(duedays))).put()

    def allof(self,query):
        return query
    def first(self,query):
        return query.first()
    def of(self,entity):
        return entity.of
    def idof(self,obj):
        return obj and obj.ID or None
    def nameof(self,obj):
        obj.__class__.__tablename__
    def columnsof(self,obj):
        for x in _inspect.get_columns(self.nameof(obj)):
            yield x['name']
    def fieldsof(self,obj):
        return {clmnm: getattr(obj,clmnm) for clmnm in self.columnsof(obj)}

    def _stored_secret(self,name):
        ass = str(
            Secret.get_or_insert(
            ID=name,
            secret=auth.make_secret()).secret)
        return ass

    def _add_student(self, studentpath=[None]*5, color=None, user=None):
        'defaults to myxxx for empty roles'
        userkey = self.of(user)
        school_, period_, teacher_, class_, student_ = studentpath
        school = self.School.get_or_insert(
            ID=school_ or 'myschool',
            userkey=userkey)
        period = self.Period.get_or_insert(
            ID=period_ or 'myperiod',
            of=school.ID,
            userkey=userkey)
        teacher = self.Teacher.get_or_insert(
            ID=teacher_ or 'myteacher',
            of=period.ID,
            userkey=userkey)
        clss = self.Class.get_or_insert(
            ID=class_ or 'myclass',
            of=teacher.ID,
            userkey=userkey)
        stdnt = self.Student.get_or_insert(
            ID=student_ or 'myself',
            of=clss.ID,
            userkey=userkey,
            color=color or '#EEE')
        if stdnt.userkey == userkey and (color and stdnt.color != color):
            stdnt.color = color
            stdnt.put()
        return stdnt

