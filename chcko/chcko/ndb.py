
##python_path()
#os.environ.update({'DATASTORE_EMULATOR_HOST': 'localhost:8081'})

from chcko.chcko.hlp import normqs, db_mixin, logger
import chcko.chcko.auth as auth

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
    token = ndb.StringProperty()
    current_role = ndb.KeyProperty(kind='Role')
    lang = ndb.StringProperty(required=False)
    created = ndb.DateTimeProperty(auto_now_add=True)

class Base(Model):
    userkey = ndb.KeyProperty(kind='User')
    created = ndb.DateTimeProperty(auto_now_add=True)

class School(Base):
    'root'
class Field(Base):
    'parent:School'
class Teacher(Base):
    'parent:Field'
class Class(Base):
    'parent: Teacher'
class Role(Base):
    'parent: Class'
    color = ndb.StringProperty()

class Problem(Base):
    'parent: Role'
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


class Assignment(Base):
    'parent: Role'
    query_string = ndb.StringProperty()
    due = ndb.DateTimeProperty()


class Index(Model):
    #id=problemid + ':' + lang
    path = ndb.StringProperty()
    knd = ndb.IntegerProperty()
    level = ndb.IntegerProperty()

class Ndb(db_mixin):
    def __init__(self):
        self.dbclient = ndb.Client()
        self.Key = ndb.Key
        self.models = {x._get_kind():x for x in [School,Field,Teacher,Class,Role,Problem,Assignment,Index,UserToken,User]}
        for k,v in self.models.items():
            setattr(self,k,v)

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
    def current_role(self,user):
        res = user.current_role and user.current_role.get()
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

    def save(self,objs):
        if isinstance(objs,list):
            ndb.put_multi(objs)
        else:
            ndb.transaction(lambda:objs.put())

    def delete_keys(self,keys):
        try:
            ndb.delete_multi(keys)
        except:
            pass #logger.info("ndb.delete_multi() failled")

    def delete_query(self,query):
        keys = query.iter(keys_only=True)
        self.delete_keys(keys)

    def filter_expression(self,ap,op,av):
        return ndb.FilterNode(ap, op, av)

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
        tosave = []
        for entry in allentries:
            edict = dict(self.itemsof(entry))
            edict['oks'] = [bool(x) for x in edict['oks']]
            cpy = anentity.create(id=entry.key.string_id(), parent=newparent.key, **edict)
            tosave.append(cpy)
        self.save(tosave)
