#def python_path():
#    d = os.path.dirname
#    local_dir = d(d(__file__))
#    if local_dir not in sys.path:
#        sys.path.insert(0, local_dir)
#python_path()

import datetime
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
            args = base64.urlsafe_b64decode(urlsafe.encode()).decode().split(',')
        tblname = lambda x: isinstance(x,str) and x or x.__tablename__
        self.strpth = tuple((tblname(args[2*i]),args[2*i+1]) for i in range(len(args)//2))
        parnt = kwargs.pop('parent',None)
        if parnt:
            self.strpth = parnt.pairs()+self.strpth
        self.pth = [(_cls[k],v) for k,v in self.strpth]
    def __eq__(self, other):
        return self.strpth == other.strpth
    def _query(self):
        jn = DBSession().query(self.pth[-1][0]).filter(self.pth[-1][0].id==self.pth[-1][1])
        for tp,qry in reversed(self.pth[:-1]):
            jn = jn.join(tp).filter(tp.id==qry)
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
        res = base64.urlsafe_b64encode(flat.encode())
        return res
    def kind(self):
        return self.pth[-1][0].__tablename__
    def parent(self):
        flat = self._flat()
        return Key(*flat[:-2])

@as_declarative(metadata=meta)
class Model(object):
    def put(self):
        DBSession().add(self)
    @classmethod
    def get_or_insert(cls,id,*args,**kwargs):
        found = DBSession().query(cls).filter(cls.id==id).first()
        if found:
            return found
        nfound = cls(id=id,*args,**kwargs)
        dbsession = DBSession()
        dbsession.begin_nested()
        try:
            dbsession.add(nfound)
            dbsession.commit()
        except IntegrityError as e:
            dbsession.rollback()
            nfound = dbsession.query(cls).filter(cls.id==id).one()
        return nfound
    @property
    def key(self):
        name = self.__class__.__table__.key
        mdls = list(_pthcls.keys())
        try:
            iname = mdls.index(name)
            rpth = []
            c = self
            while iname>=0:
                rpth += [c.id,mdls[iname]]
                iname = iname - 1
                if iname>=0:
                    _c = _cls[mdls[iname]]
                    c = DBSession().query(_c).filter(_c.id==c.of).first()
                    if not c:
                        break
            flat = list(reversed(rpth))
            res = Key(*flat)
        except:
            res = Key(name,self.id)
        return res
    @declared_attr
    def __tablename__(cls):
        return cls.__name__
    @declared_attr
    def __table_args__(cls):
        return {'extend_existing':True}
    id=C(String,primary_key=True,autoincrement=False)

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
        token = token or auth.gen_salt()
        key = cls.selfmadekey(subject, token)
        entity = cls(id=key.string_id(), email=email, subject=subject, token=token)
        entity.put()
        return entity
class User(Model):
    fullname = C(String)
    pwhash = C(String)
    token_model = C(ForeignKey('UserToken.id'))
    current_student = C(ForeignKey('Student.id',use_alter=True))
    def set_password(self, password):
        self.pwhash = auth.generate_password_hash(password)
    @classmethod
    def create(cls, email, password):
        user = cls.by_login(email,password)
        if not user:
            user = cls.get_or_insert(email, pwhash=auth.generate_password_hash(password))
        return user
    @classmethod
    def by_login(cls,email,password):
        user = Key(cls,email).get()
        if user:
            if not auth.check_password_hash(user.pwhash,password):
                return None
        return user
    @hybrid_property
    def email(self):
        return self.id
class Secret(Model):  # filled manually
    secret = C(String)


class School(Model):
    userkey = C(ForeignKey('User.id'))
    created = C(DateTime,default=datetime.datetime.now)
class Period(Model):
    userkey = C(ForeignKey('User.id'))
    created = C(DateTime,default=datetime.datetime.now)
    of = C(ForeignKey('School.id'))
class Teacher(Model):
    userkey = C(ForeignKey('User.id'))
    created = C(DateTime,default=datetime.datetime.now)
    of = C(ForeignKey('Period.id'))
class Class(Model):
    userkey = C(ForeignKey('User.id'))
    created = C(DateTime,default=datetime.datetime.now)
    of = C(ForeignKey('Teacher.id'))
class Student(Model):
    userkey = C(ForeignKey('User.id'))
    created = C(DateTime,default=datetime.datetime.now)
    of = C(ForeignKey('Class.id'))
    color = C(String)
class Problem(Model):
    userkey = C(ForeignKey('User.id'))
    of = C(ForeignKey('Student.id'))
    query_string = C(String)
    lang = C(String)
    # the numbers randomly chosen, in python dict format
    given = C(PickleType)
    created = C(DateTime,default=datetime.datetime.now)
    answered = C(DateTime)
    # links to a collection: 1-n, p.problem_set.get()!
    collection = C(ForeignKey('Problem.id'))


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
    userkey = C(ForeignKey('User.id'))
    created = C(DateTime,default=datetime.datetime.now)
    of = C(ForeignKey('Student.id'))
    query_string = C(String)
    due = C(DateTime)

class Index(Model):
    path = C(String)
    knd = C(Integer)
    level = C(Integer)


meta.create_all()

class Counter(object):
    def __init__(self, value=0):
        self.val = value
        self.lock = threading.Lock()
    def __call__(self):
        with self.lock:
            self.val += 1
            return str(self.val)
cntproblem = Counter(0)
cntassignment = Counter(0)


_cls = {x.__tablename__:x for x in [School,Period,Teacher,Class,Student,Problem,Assignment,Index,UserToken,User,Secret]}
_pthcls = {'School':School, 'Period':Period, 'Teacher':Teacher, 'Class':Class, 'Student':Student, 'Problem':Problem}
_inspect = inspect(engine)
_probcols = [x['name'] for x in _inspect.get_columns('Problem')]
_probkey = set("of created lang query_string nr".split())

class Sql(db_mixin):
    def __init__(self):
        self.dbclient = Client()
        self.Key = Key
        for k,v in _cls.items():
            setattr(self,k,v)
        self.init_db()

    def is_sql(self):
        return True
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
    def problem_create(self,student,**pkwargs):
        params = {s: pkwargs[s] for s in _probcols if s in pkwargs}
        probid = cntproblem()
        return self.Problem(id=probid, of=student.id, **params)
    def _copy_to_new_parent(self, entity, oldparent, newparent):
        self.query(entity,[self.of(entity)==self.idof(oldparent)]).update(
            {'of':newparent.id},synchronize_session=False)
    def assign_to_student(self, studentkeyurlsafe, query_string, duedays):
        now = datetime.datetime.now()
        studentkey = self.Key(urlsafe=studentkeyurlsafe)
        params = dict(of=studentkey.string_id(), query_string=normqs(query_string),
                   due=now + datetime.timedelta(days=int(duedays)))
        assid = cntassignment()
        asgn = Assignment(id=assid, **params)
        asgn.put()

    def allof(self,query):
        return query.all()
    def first(self,query):
        return query.first()
    def of(self,oe):
        return oe.of
    def idof(self,obj):
        return obj.id
    def nameof(self,obj):
        return obj.__class__.__tablename__
    def columnsof(self,obj):
        for x in _inspect.get_columns(self.nameof(obj)):
            yield x['name']
    def fieldsof(self,obj):
        return {clmnm: getattr(obj,clmnm) for clmnm in self.columnsof(obj)}
    def add_to_set(self,problem,other):
        problem.collection = other.id

    def add_student(self, studentpath=[None]*5, color=None, user=None):
        'defaults to myxxx for empty roles'
        userkey = user and self.idof(user) or None
        school_, period_, teacher_, class_, student_ = studentpath
        school = self.School.get_or_insert(
            school_ or 'myschool',
            userkey=userkey)
        period = self.Period.get_or_insert(
            period_ or 'myperiod',
            of=school.id,
            userkey=userkey)
        teacher = self.Teacher.get_or_insert(
            teacher_ or 'myteacher',
            of=period.id,
            userkey=userkey)
        clss = self.Class.get_or_insert(
            class_ or 'myclass',
            of=teacher.id,
            userkey=userkey)
        stdnt = self.Student.get_or_insert(
            student_ or 'myself',
            of=clss.id,
            userkey=userkey,
            color=color or '#EEE')
        if stdnt.userkey == userkey and (color and stdnt.color != color):
            stdnt.color = color
            stdnt.put()
        return stdnt

    def user_name(self,user):
        return user.fullname or user.id

