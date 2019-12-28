
##python_path()
#os.environ.update({'DATASTORE_EMULATOR_HOST': 'localhost:8081'})
import datetime

from chcko.hlp import normqs, db_mixin
import chcko.auth as auth

from google.cloud import ndb

class Base(ndb.Model):
    userkey = ndb.KeyProperty(kind='User')
    created = ndb.DateTimeProperty(auto_now_add=True)

class School(Base):
    'root'
class Period(Base):
    'parent:School'
class Teacher(Base):
    'parent:Period'
class Class(Base):
    'parent: Teacher'
class Student(Base):
    'parent: Class'
    color = ndb.StringProperty()

class Problem(Base):
    'parent: Student'
    query_string = ndb.StringProperty()
    lang = ndb.StringProperty()
    # the numbers randomly chosen, in python dict format
    given = ndb.PickleProperty()
    #created already in Base
    answered = ndb.DateTimeProperty()
    # links to a collection: 1-n, p.problem_set.get()!
    collection = ndb.KeyProperty(kind='Problem')
    # a list of names given to the questions (e.g '1','2')
    inputids = ndb.StringProperty(repeated=True)
    # calculated from given, then standard formatted to strings
    results = ndb.StringProperty(repeated=True)
    oks = ndb.BooleanProperty(repeated=True)
    points = ndb.IntegerProperty(repeated=True)  # points for this sub-problem
    # standard formatted from input
    answers = ndb.StringProperty(repeated=True)
    nr = ndb.IntegerProperty()  # needed to restore order
    answersempty = ndb.ComputedProperty(lambda self: ''.join(self.answers) == '')
    link = ndb.ComputedProperty(lambda self: '/'+self.lang+'/content?'+self.query_string)


class Assignment(Base):
    'parent: Student'
    query_string = ndb.StringProperty()
    due = ndb.DateTimeProperty()


class Index(ndb.Model):
    path = ndb.StringProperty()
    knd = ndb.IntegerProperty()
    level = ndb.IntegerProperty()


class UserToken(ndb.Model):
    subject = ndb.StringProperty(required=True) #signup or auth
    token = ndb.StringProperty(required=True)
    email = ndb.StringProperty(required=False)
    created = ndb.DateTimeProperty(auto_now_add=True)
    updated = ndb.DateTimeProperty(auto_now=True)
    @classmethod
    def selfmadekey(cls, subject, token):
        return ndb.Key(cls, '%s.%s' % (subject, token))
    @classmethod
    def create(cls, email, subject, token=None):
        email = email
        token = token or auth.gen_salt()
        key = cls.selfmadekey(subject, token)
        entity = cls(key=key, email=email, subject=subject, token=token)
        entity.put()
        return entity
class User(ndb.Model):
    fullname = ndb.StringProperty(required=False)
    pwhash = ndb.StringProperty(required=False)
    token_model = ndb.StructuredProperty(UserToken)
    current_student = ndb.KeyProperty(kind='Student')
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
        user = ndb.Key(cls,email).get()
        if user:
            if not auth.check_password_hash(user.pwhash,password):
                return None
        return user
class Secret(ndb.Model):  # filled manually
    secret = ndb.StringProperty()

_cls = {x._get_kind():x for x in [School,Period,Teacher,Class,Student,Problem,Assignment,Index,UserToken,User,Secret]}
_pthcls = {'School':School, 'Period':Period, 'Teacher':Teacher, 'Class':Class, 'Student':Student, 'Problem':Problem}
_probcols = [k for k, v in Problem._properties.items() if isinstance(v, ndb.ComputedProperty)]

#dbclient=ndb.Client('chcko')
#c = dbclient.context
#
#ut=UserToken()
#ut.subject="signup"
#ut.email="email1"
#ut.token="tokn"
#with c():
#  ut.put()
#with c(): print(UserToken.query().count()) #1
#with c(): print(UserToken.query().fetch(1)[0].key) #None            #Key('UserToken', 1)
#with c(): print(UserToken.query().fetch(1)[0].key.integer_id())     #1
#with c(): print(UserToken.query().fetch(1)[0].key.string_id())      #None
#with c(): print(UserToken.query().fetch(1)[0].key.id())             #1
#with c(): k=UserToken.query(UserToken.email=='email1')              #
#with c(): nv=k.get()                                                #
#with c(): print(nv.subject,nv.email)                                #signup email1
#with c(): k=ndb.Key('UserToken',1)                                  #
#with c(): nv=k.get()                                                #
#with c(): print(nv.subject,nv.email)                                #signup email1
#with c(): print(k.pairs())                                          #(('UserToken', 1),)
#with c(): print(k.urlsafe())                                        #b'agVjaGNrb3IPCxIJVXNlclRva2VuGAEM'
#with c(): print(nv.key.pairs())                                     #(('UserToken', 1),)
#with c(): print(nv.key.kind())                                      #UserToken


class Ndb(db_mixin):
    def __init__(self):
        self.dbclient = ndb.Client('chcko')
        self.Key = ndb.Key
        for k,v in _cls.items():
            setattr(self,k,v)
        self.init_db()

    def is_sql(self):
        return False
    def query(self,entity,filt=None,ordr=None):
        _filt = filt or []
        q = entity.query(*_filt)
        if ordr:
            q = q.order(ordr)
        return q
    def delete(self,query):
        ndb.delete_multi(query.iter(keys_only=True))
    def filter_expression(self,ap,op,av):
        return ndb.FilterNode(ap, op, av)
    #def problem_by_query_string(self,query_string,lang,student):
    #    q = Problem.gql( #TODO: does gql still work with Python 3
    #        "WHERE query_string = :1 AND lang = :2 AND answered = NULL AND ANCESTOR IS :3",
    #        query_string, lang, student.key)
    #    fch = q.fetch(1)
    #    return fch[0] if fch else None
    #def clear_unanswered_problems(self):
    #    self.delete(Problem.gql("WHERE answered = NULL"))
    #def del_stale_open_problems(self,student,age):
    #    self.delete(Problem.gql(
    #        "WHERE answered = NULL AND created < :1 AND ANCESTOR IS :2",
    #        age,
    #        self.request.student.key))
    #    self.delete(Problem.gql(
    #        "WHERE answersempty = True AND answered != NULL AND ANCESTOR IS :1",
    #        self.request.student.key))
    def problem_create(self,student,**pkwargs):
        return self.Problem(parent=student.key,
                  **{s: pkwargs[s] for s in self.Problem._properties if s in pkwargs})
    def _copy_to_new_parent(self, anentity, oldparent, newparent):
        for entry in self.allof(anentity.query(parent=oldparent.key)):
            cpy = anentity(id=entry.key.string_id(), parent=newparent.key)
            cpy.populate(**{k: v for k, v in entry.to_dict().items() if k in _probcols})
            cpy.put()
    def assign_to_student(self, studentkeyurlsafe, query_string, duedays):
        now = datetime.datetime.now()
        studentkey = self.Key(urlsafe=studentkeyurlsafe)
        Assignment(parent=studentkey, query_string=normqs(query_string),
                   due=now + datetime.timedelta(days=int(duedays))).put()

    def allof(self,query):
        return query.iter()
    def first(self,query):
        return query.get()
    def of(self,entity):
        return entity.parent
    def idof(self,obj):
        return obj.key
    def nameof(self,entity):
        return entity._get_kind()
    def columnsof(self,obj):
        return entity._properties.keys()
    def fieldsof(self,entity):
        return {s: v.__get__(entity) for s,v in entity._properties.items()}
    def add_to_set(self,problem,other):
        problem.collection = other.key

    def add_student(self, studentpath=[None]*5, color=None, user=None):
        'defaults to myxxx for empty roles'
        userkey = user and self.idof(user) or None
        school_, period_, teacher_, class_, student_ = studentpath
        school = self.School.get_or_insert(
            school_ or 'myschool',
            userkey=userkey)
        period = self.Period.get_or_insert(
            period_ or 'myperiod',
            parent=school.key,
            userkey=userkey)
        teacher = self.Teacher.get_or_insert(
            teacher_ or 'myteacher',
            parent=period.key,
            userkey=userkey)
        clss = self.Class.get_or_insert(
            class_ or 'myclass',
            parent=teacher.key,
            userkey=userkey)
        stdnt = self.Student.get_or_insert(
            student_ or 'myself',
            parent=clss.key,
            userkey=userkey,
            color=color or '#EEE')
        if stdnt.userkey == userkey and (color and stdnt.color != color):
            stdnt.color = color
            stdnt.put()
        return stdnt

    def user_name(self,user):
        return user.fullname or user.key.string_id()
