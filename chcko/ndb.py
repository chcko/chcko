
##python_path()
#os.environ.update({'DATASTORE_EMULATOR_HOST': 'localhost:8081'})

from chcko.hlp import normqs, db_mixin
import chcko.auth as auth

from google.cloud import ndb

class Model(ndb.Model):
    @classmethod
    def create(cls,**kwargs):
        return cls(**kwargs)

class UserToken(Model):
    email = ndb.StringProperty(required=False)
    created = ndb.DateTimeProperty(auto_now_add=True)
    updated = ndb.DateTimeProperty(auto_now=True)
class User(Model):
    fullname = ndb.StringProperty(required=False)
    pwhash = ndb.StringProperty(required=False)
    verified = ndb.IntegerProperty()
    token_model = ndb.StructuredProperty(UserToken)
    current_student = ndb.KeyProperty(kind='Student')
class Secret(Model):  # filled manually
    secret = ndb.StringProperty()

class Base(Model):
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
    concatanswers = ndb.StringProperty() #concat duplicate of answers (set_answer)
    @property
    def link(self):
        return '/' + self.lang + '/content?' + self.query_string


class Assignment(Base):
    'parent: Student'
    query_string = ndb.StringProperty()
    due = ndb.DateTimeProperty()


class Index(Model):
    path = ndb.StringProperty()
    knd = ndb.IntegerProperty()
    level = ndb.IntegerProperty()

_cls = {x._get_kind():x for x in [School,Period,Teacher,Class,Student,Problem,Assignment,Index,UserToken,User,Secret]}

class Ndb(db_mixin):
    def __init__(self):
        self.dbclient = ndb.Client('chcko')
        self.Key = ndb.Key
        for k,v in _cls.items():
            setattr(self,k,v)
        self.models = _cls
        self.init_db()

    def is_sql(self):
        return False
    def allof(self,query):
        return list(query.iter())
    def first(self,query):
        return query.get()
    def idof(self,obj):
        return obj.key if obj else None
    def kindof(self,entity):
        return entity._get_kind()
    def columnsof(self,entity):
        return entity._properties.keys()
    def itemsof(self,entry):
        return entry.to_dict().items()
    def nameof(self,obj):
        return obj.key.string_id()
    def fieldsof(self,entity):
        return {s: v.__get__(entity) for s,v in entity._properties.items()}
    def add_to_set(self,problem,other):
        problem.collection = other.key
    def current_student(self,user):
        res = user.current_student and user.current_student.get()
        return res

    def urlsafe(self,key):
        res = key.urlsafe()
        res = res.decode()
        return res

    def query(self,entity,filt=None,ordr=None,parent=None):
        _filt = filt or []
        if parent:
            q = entity.query(*_filt,ancestor=parent)
        else:
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
    #        "WHERE concatanswers = '' AND answered != NULL AND ANCESTOR IS :1",
    #        self.request.student.key))


    def keys_below(self,parent): #only used in testing, not availabe for sql
        return ndb.Query(ancestor=parent.key).iter(keys_only=True)

    def done_assignment(self,assignm):
        student = assignm.key.parent()
        q = self.query(self.Problem, [self.Problem.query_string == normqs(assignm.query_string),
                                 self.Problem.answered > assignm.created], parent = student)
        if q.count() > 0:
            return True
        else:
            return False

    def copy_to_new_parent(self, anentity, oldparent, newparent):
        clms = self.columnsof(anentity)
        allentries = self.allof(self.query(anentity,parent=self.idof(oldparent)))
        for entry in allentries:
            edict = dict(self.itemsof(entry))
            edict['oks'] = [bool(x) for x in edict['oks']]
            cpy = anentity.create(id=entry.key.string_id(), parent=newparent.key, **edict)
            cpy.put()
