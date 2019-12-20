import datetime
import time
from itertools import chain
from bottle import SimpleTemplate

from chcko.hlp import key_value_leaf_id, datefmt, normqs, filter_student
from chcko.languages import langkindnum, langnumkind, kindint
import chcko.auth as auth

from sqlalchemy.ext.declarative import as_declarative
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.ext.declarative.api import declared_attr
from sqlalchemy.schema import CreateColumn
from sqlalchemy.ext.compiler import compiles
from sqlalchemy.orm.mapper import Mapper
from sqlalchemy import *
C = Column

#TODO move
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
engine = create_engine("sqlite://")
session = Session(engine)
meta = MetaData(engine)

@compiles(CreateColumn)
def computed_column(element, compiler, **kw):
    col = element.element
    result = compiler.visit_create_column(element, **kw)
    if "computed" in col.info:
        result += " AS (%s) STORED" % col.info["computed"]
    return result

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
        entity = cls(key=key, email=email, subject=subject, token=token)
        entity.put()
        return entity
class User(Model):
    email = C(String,nullable=False)
    pwhash = C(String)
    token_model = C(ForeignKey('UserToken.ID'))
    current_student = C(ForeignKey('Student.ID'),use_alter=True)
    def set_password(self, password):
        self.pwhash = generate_password_hash(password)
    @classmethod
    def create(cls, email, password):
        user = cls.by_login(email,password)
        if not user:
            user = cls.get_or_insert(email=email, pwhash=generate_password_hash(password))
        return user
    @classmethod
    def by_login(cls,email,password):
        user = Key(cls,email).get()
        if user:
            if not check_password_hash(user.pwhash,password):
                return None
        return user
class Secret(Model):  # filled manually
    secret = C(String)


class School(Model):
    userkey = C(ForeignKey('User.ID'))
    created = C(DateTime,default=datetime.datetime.now)
class Period(Model):
    userkey = C(ForeignKey('User.ID'))
    created = C(DateTime,default=datetime.datetime.now)
    parent = C(ForeignKey('School.ID'))
class Teacher(Model):
    userkey = C(ForeignKey('User.ID'))
    created = C(DateTime,default=datetime.datetime.now)
    parent = C(ForeignKey('Period.ID'))
class Class(Model):
    userkey = C(ForeignKey('User.ID'))
    created = C(DateTime,default=datetime.datetime.now)
    parent = C(ForeignKey('Teacher.ID'))
class Student(Model):
    userkey = C(ForeignKey('User.ID'))
    created = C(DateTime,default=datetime.datetime.now)
    parent = C(ForeignKey('Class.ID'))
    color = C(String)
class Problem(Model):
    userkey = C(ForeignKey('User.ID'))
    parent = C(ForeignKey('Student.ID'))
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
    parent = C(ForeignKey('Student.ID'))
    query_string = C(String)
    due = C(DateTime)

class Index(Model):
    path = C(String)
    knd = C(Integer)
    level = C(Integer)

#TODO move
meta.create_all()
#ie=inspect(engine)
#ie.get_table_names()
#ie.get_columns('School')
#ut=UserToken()
#ut.ID="1"
#ut.subject="signup"
#ut.email="email1"
#ut.token="tokn"
##UserToken.__table__.create()
#ut2=UserToken(ID='2',subject='auth',email='email2',token='tokn2')
#session.add(ut2)
#session.commit()
#session.Query=session.query
#make ndb=session
#session.Query(UserToken).filter(and_(UserToken.subject=='auth',UserToken.email=='email2')).one().token
##session.rollback()

#### CONTINUE

class Key:
    '''A key is like a word in the sense that it is an address to the entity.
    It has more views, though
    It provides:
    __init__(urlsafe=xxx)
    __init__(Model1,ID1, Model2,ID2,...) #Model can be class or class name
    pairs() id() string_id() urlsafe() kind() parent() get() delete() urlstring()
    '''
    _name_table = {x.__tablename__:x for x in [School,Period,Teacher,Class,Student,Problem,Assignment,Index,UserToken,User,Secret]}
    def __init__(*args):
        #args = [UserToken,and_(UserToken.subject=='signup',UserToken.email=='email')]
        #args = [UserToken,UserToken.ID=='1']
        tblname = lambda x: isinstance(x,str) and x or x.__tablename__
        self_k = [(tblname(args[i]),args[i+1]) for i in range(len(args)//2)]
        self_k = [(_name_table[k],v) for k,v in self_k]
    def get():
        e = self_k[0]
        session.query(e[0]).filter(e[1]).one()

    def pairs():

    def urlstring(self):
        '''
        >>> myself.key.urlstring()
        'School=myschool&Period=myperiod&Teacher=myteacher&Class=myclass&Student=myself'

        '''
        return '&'.join([r + '=' + str(v) for r, v in self.pairs()])


class Sql:
    ''' provides interface of ndb.Ndb using SqlAlchemy
    TODO
    '''
    models = {'School':School, 'Period':Period, 'Teacher':Teacher, 'Class':Class, 'Student':Student, 'Problem':Problem}
    def __init__(self):
        import initdb
        self.available_langs = initdb.available_langs
        with self.ctx.context():
            self.clear_students()
            self.student_contexts = list(models.keys())[:-1]
            self.problem_contexts = list(models.keys())
            initdb.populate_index(
                lambda query, lang, kind, level, path:
                    Index.get_or_insert(
                        query + ':' + lang,
                        knd=int(kind),
                        level=int(level),
                        path=path)
            )

    def _have_one_non_random_student(self):
        self.myschool = School.get_or_insert('myschool')
        self.myperiod = Period.get_or_insert('myperiod', parent=myschool.key)
        self.myteacher = Teacher.get_or_insert('myteacher', parent=myperiod.key)
        self.myclass = Class.get_or_insert('myclass', parent=myteacher.key)
        self.myself = Student.get_or_insert('myself', parent=myclass.key)
    def _delete(self,query):
        sql.delete_multi(query.iter(keys_only=True))

    def key_from_path(self,x):
        return Key(*list(chain(*zip(self.problem_contexts[:len(x)], x))))
    def from_urlsafe(urlsafe):
        return Key(urlsafe=urlsafe).get()
    def clear_index(self):
        self._delete(Index.query())
    def clear_problems(self):
        self._delete(Problem.query())
    def problem_set(self,problem):
        Problem.query(Problem.collection==problem.key).order(Problem.nr)
    def problem_by_query_string(self,query_string,lang,student):
        q = Problem.gql(
            "WHERE query_string = :1 AND lang = :2 AND answered = NULL AND ANCESTOR IS :3",
            query_string, lang, student.key)
        fch = q.fetch(1)
        return fch[0] if fch else None
    def problem_from_resolver(self, rsv, nr, student):
        '''create a problem from a resolver (see hlp.py)
        '''
        d = rsv.load()
        g = d.given()
        r = d.norm(d.calc(g))
        pkwargs = d.__dict__.copy()
        pkwargs.update(dict(
            g=g,
            answered=None,
            lang=rsv.lang,
            query_string=rsv.query_string,
            nr=nr,
            results=r,
            given=g,
            inputids=["{:0=4x}".format(nr) + "_{:0=4x}".format(a) for a in range(len(r))],
            points=d.points or [1] * len(r or [])
        ))
        problem = Problem(parent=student.key,
                      **{s: pkwargs[s] for s,
                         v in Problem._properties.items() if s in pkwargs})
        return problem, pkwargs
    def clear_unanswered_problems(self):
        self._delete(Problem.gql("WHERE answered = NULL"))
    def clear_assignments(self):
        self._delete(Assignment.query())
    def clear_students(self):
        self._delete(Student.query())
        self._delete(Class.query())
        self._delete(Teacher.query())
        self._delete(Period.query())
        self._delete(School.query())
        _have_one_non_random_student(self):
    def clear_student_problems(self,student):
        self._delete(Problem.query(ancestor=student.key))
    def student_assignments(self,student):
        return Assignment.query(ancestor=student.key)
    def clear_student_assignments(self,student):
        self._delete(student_assignments(ancestor=student.key))
    def del_stale_open_problems(self,student,age):
        self._delete(Problem.gql(
            "WHERE answered = NULL AND created < :1 AND ANCESTOR IS :2",
            age,
            self.request.student.key))
        self._delete(Problem.gql(
            "WHERE answersempty = True AND answered != NULL AND ANCESTOR IS :1",
            self.request.student.key))
    def del_collection(self,problem):
        self._delete(Problem.query(Problem.collection==problem.key))
        problem.key.delete()
    def _copy_to_new_parent(self, anentity, oldparent, newparent):
        '''copy all instances of an entity from an old parent to a new one'''
        computed = [k for k, v in anentity._properties.iteritems()
                    if isinstance(v, ndb.ComputedProperty)]
        for entry in anentity.query(ancestor=oldparent.key).iter():
            cpy = anentity(id=entry.key.string_id(), parent=newparent.key)
            cpy.populate(**{k: v for k, v in entry.to_dict().items()
                            if k not in computed})
            cpy.put()
    deff copy_to_new_student(self,oldparent, newparent):
        self._copy_to_new_parent(Problem, oldstudent, self.request.student)
        self._copy_to_new_parent(Assignment, oldstudent, self.request.student)
    def assign_to_student(self, studentkeyurlsafe, query_string, duedays):
        now = datetime.datetime.now()
        studentkey = Key(urlsafe=studentkeyurlsafe)
        Assignment(parent=studentkey, query_string=normqs(query_string),
                   due=now + datetime.timedelta(days=int(duedays))).put()
    def done_assignment(self,akey):
        'check if assignment has been answered after its creation time'
        if not akey:
            return False
        assignm = akey.get()
        q = Problem.query(
            ancestor=akey.parent()).filter(
            Problem.query_string == normqs(
                assignm.query_string),
            Problem.answered > assignm.created)
        if q.count() > 0:
            return True
        else:
            return False
    def clear_done_assignments(self, student, user):
        for akey in self.assign_table(student, user):
            if done_assignment(akey):
                akey.delete()
    def assignable(self, teacher, user):
        for akey in depth_1st(keys=[teacher.key], kinds='Teacher Class Student'.split(),
                              userkey=user and user.key):
            yield akey
    def assign_table(student, user):
        for e in depth_1st(keys=[student.key], models='Student Assignment'.split(),
                           userkey=user and user.key):
            yield e
    def key_ownd_path(self, student, user):
        userkey = user and user.key
        key_ownd_list = [(student.key, student.userkey == userkey)]
        parent = student.parent()
        while parent:
            key_ownd_list = [(parent.key, parent.userkey == userkey)] + key_ownd_list
            parent = parent.parent()
        return key_ownd_list
    def student_roles(self, user):
        userkey = user and user.key
        students = Student.query(
            Student.userkey == userkey).iter()
        for student in students:
            yield self.key_ownd_path(student, user)

    def keys_to_omit(self,path):
        "[name1,name2,nonstr,...]->[key2,key2]"
        keys = []
        pth = [isinstance(x, str) for x in path]
        ipth = pth.index(False) if False in pth else len(pth)
        if ipth > 0:
            keys = [self.key_from_path(path[:ipth])] * ipth
        return keys
    def nameof(entity):
        entity._get_kind()
    def fieldsof(entity):
        return {s: v.__get__(entity) for s,v in entity._properties.items()}
    def tree_keys(parent): #only used in testing
        return ndb.Query(ancestor=parent.key).iter(keys_only=True)
    def depth_1st(self
                  , path=None
                  , keys=None  # start keys, keys_to_omit(path) to skip initial hierarchy
                  , kinds=self.problem_contexts
                  , permission=False
                  , userkey=None
                  ):
        ''' path entries are names or filters ([] for all)
        translated into keys along the levels given by **kinds** depth-1st-wise.

        >>> from chcko.db import *
        >>> from chcko.test.hlp import problems_for
        >>> #del sys.modules['chcko.test.hlp']
        >>> path = ['a', 'b', 'c', 'd', 'e']
        >>> student = _add_student(path, 'EEE')
        >>> problems_for(student)
        >>> lst = list(db.depth_1st(path+[[]]))
        >>> db.nameof([k.get() for k in list(db.depth_1st(path+[[('query_string','=','r.u')]]))][0])
        'School'
        >>> path = ['a', 'b', 'c', 'x', 'e']
        >>> student1 = _add_student(path, 'EEE')
        >>> problems_for(student1)
        >>> path = ['a','b','c',[],[],[('query_string','=','r.u')]]
        >>> list(db.depth_1st(path))[0].kind()
        'School'
        >>> list(db.depth_1st(path,keys=db.keys_to_omit(path)))[0].kind()
        'Class'
        >>> list(db.depth_1st())
        []

        '''
        modelclasses = [models[name] for name in kinds]
        N = len(modelclasses)
        if not path:
            path = [[]] * N
        while len(path) < N:
            path += [[]]
        if keys is None:
            keys = []
        i = len(keys)
        parentkey = keys and keys[-1] or None
        permission = permission or parentkey and parentkey.get().userkey == userkey
        if isinstance(path[i], str):
            k = Key(modelclasses[i]._get_kind(), path[i], parent=parentkey)
            if k:
                yield k
                if i < N - 1:
                    keys.append(k)
                    for e in depth_1st(path, keys, kinds, permission, userkey):
                        yield e
                    del keys[-1]
        elif permission:
            q = modelclasses[i].query(ancestor=parentkey)
            #q = Assignment.query(ancestor=studentkey)
            if modelclasses[i] == Problem:
                q = q.order(Problem.answered)
            elif 'created' in modelclasses[i]._properties:
                q = q.order(modelclasses[i].created)
            for ap, op, av in path[i]:
                if ap in modelclasses[i]._properties:
                    fn = ndb.FilterNode(ap, op, av)
                    q = q.filter(fn)
            #qiter = q.iter(keys_only=True)
            for k in q.iter(keys_only=True):
                # k=next(qiter)
                yield k
                if i < N - 1:
                    keys.append(k)
                    for e in depth_1st(path, keys, kinds, permission):
                        yield e
                    del keys[-1]
        # else:
        # yield None #no permission or no such object

    def _stored_secret(self,name):
        ass = str(
            Secret.get_or_insert(
            name,
            secret=auth.make_secret()).secret)
        return ass
    def stored_email_credential(self):
        return base64.urlsafe_b64decode(_stored_secret('chcko.mail').encode())
    def user_timestamp_by_token(self, token, subject='auth'):
        usertoken = User.token_model.selfmadekey(subject, token).get()
        if usertoken:
            user = Key(User, usertoken.email).get()
            if user:
                timestamp = int(time.mktime(usertoken.created.timetuple()))
                return user, timestamp
        return None, None
    def create_signup_token(self, email):
        return UserToken.create(email, 'signup').token
    def delete_signup_token(self, token):
        UserToken.selfmadekey('signup', token).delete()
    def create_user(self,email,password):
        return User.create(email,password)
    def user_by_login(self,email,password):
        return User.by_login(email,password)
    def validate_token(self,subject, token):
        return UserToken.selfmadekey(subject=subject,
                   token=token).get() is not None
    def validate_signup_token(self, token):
        return self.validate_token('signup', token)

    def filtered_index(self, lang, opt):
        ''' filters the index by lang and optional by

            - level
            - kind
            - path
            - link

        >>> from chcko.db import *
        >>> lang = 'en'
        >>> opt1 = [] #[('level', '2'), ('kind', 'exercise')]
        >>> cnt1 = sum([len(list(gen[1])) for gen in db.filtered_index(lang, opt1)])
        >>> opt2 = [('level', '10'),('kind','1'),('path','maths'),('link','r')]
        >>> cnt2 = sum([len(list(gen[1])) for gen in db.filtered_index(lang, opt2)])
        >>> cnt1 != 0 and cnt2 != 0 and cnt1 > cnt2
        True

        '''
        def safeint(s):
            try:
                return int(s)
            except:
                return -1
        kindnum = langkindnum[lang]
        numkind = langnumkind[lang]
        optd = dict(opt)
        knd_pathlnklvl = {}
        itr = Index.query().iter()
        for e in itr:
            # e=itr.next()
            # knd_pathlnklvl
            link, lng = e.key.string_id().split(':')
            if lng == lang:
                if 'level' not in optd or safeint(optd['level']) == e.level:
                    if 'kind' not in optd or kindint(optd['kind'],kindnum) == e.knd:
                        if 'path' not in optd or optd['path'] in e.path:
                            if 'link' not in optd or optd['link'] in link:
                                lpl = knd_pathlnklvl.setdefault(e.knd, [])
                                lpl.append((e.path, (link, e.level)))
                                lpl.sort()
        s_pl = sorted(knd_pathlnklvl.items())
        knd_pl = [(numkind[k], key_value_leaf_id(v)) for k, v in s_pl]
        #[('Problems', <generator>), ('Content', <generator>),... ]
        return knd_pl

    def table_entry(self, e):
        'what of entity e is used to render html tables'
        if isinstance(e, Problem) and e.answered:
            problem_set = Problem.query(
                Problem.collection == e.key).order(
                Problem.nr)
            if problem_set.count():
                return [datefmt(e.answered), e.answers]
            else:
                return [datefmt(e.answered), e.oks, e.answers, e.results]
        elif isinstance(e, Student):
            return ['', '', '', '', e.key.string_id()]
        elif isinstance(e, Class):
            return ['', '', '', e.key.string_id()]
        elif isinstance(e, Teacher):
            return ['', '', e.key.string_id()]
        elif isinstance(e, Period):
            return ['', e.key.string_id()]
        elif isinstance(e, School):
            return [e.key.string_id()]
        elif isinstance(e, Assignment):
            now = datetime.datetime.now()
            overdue = now > e.due
            return [(datefmt(e.created), e.query_string), datefmt(e.due), overdue]
        # elif e is None:
        #    return ['no such object or no permission']
        return []


    def set_user(self,request):
        session = request.session
        userID = session and session['userID']
        request.user = None
        if userID:
            request.user = Key(urlsafe=userID).get()

    def set_student(self,request):
        '''There is always a student role

        - There is a student role per client without user
        - There are more student roles for a user with one being current

        Else a redirect string for a message is returned.

        '''
        user = request.user
        userkey = user and user.key
        session = request.session
        request.student = None
        studentpath = [request.get(x,'') for x in self.student_contexts]
        color = request.get('color','')
        request.query_string = filter_student(request.query_string)
        if ''.join(studentpath) != '':
            student = self._add_student(studentpath, color, user)
            if student.userkey == userkey):
                request.student = student
            # student role does not belong to user, so don't change current student
            else:
                return 'message?msg=e'
        elif user:
            request.student = user.current_student and user.current_student.get()
        else:
            studentkey_nouser = session and Session['studentkey_nouser']
            if studentkey_nouser:
                try:
                    request.student = Key(
                        urlsafe=studentkey_nouser).get()
                except (TypeError, BadKeyError, AttributeError):
                    pass
        if not request.student and user:
            request.student = Student.query(Student.userkey == userkey).get()
        if not request.student:  # generate
            studentpath = auth.random_student_path(seed=request.remote_addr).split('-')
            request.student = self._add_student(studentpath, color, user)
        if user:
            if user.current_student != request.student.key:
                user.current_student = request.student.key
                user.put()
        elif session:
            session['studentkey_nouser'] = request.student.key.urlsafe()
        SimpleTemplate.defaults.update(models)
        SimpleTemplate.defaults["contextcolor"] = request.student.color or '#EEE'
        SimpleTemplate.defaults["key_from_path"] = key_from_path

    def _add_student(self, studentpath, color=None, user=None):
        'defaults to myxxx for empty roles'
        userkey = user and user.key
        school_, period_, teacher_, class_, student_ = studentpath
        school = School.get_or_insert(
            school_ or 'myschool',
            userkey=userkey)
        period = Period.get_or_insert(
            period_ or 'myperiod',
            parent=school.key,
            userkey=userkey)
        teacher = Teacher.get_or_insert(
            teacher_ or 'myteacher',
            parent=period.key,
            userkey=userkey)
        clss = Class.get_or_insert(
            class_ or 'myclass',
            parent=teacher.key,
            userkey=userkey)
        stdnt = Student.get_or_insert(
            student_ or 'myself',
            parent=clss.key,
            userkey=userkey,
            color=color or '#EEE')
        if stdnt.userkey == userkey and (color and stdnt.color != color):
            stdnt.color = color
            stdnt.put()
        return stdnt

    def send_mail(self, to, subject, message_text, creds, sender=chcko_mail):
        auth.send_mail(to, subject, message_text, creds=self.stored_email_credential())








from sqlalchemy import Column
from sqlalchemy import create_engine
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import backref
from sqlalchemy.orm import joinedload_all
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Session
from sqlalchemy.orm.collections import attribute_mapped_collection


Base = declarative_base()


class TreeNode(Base):
    __tablename__ = "tree"
    id = Column(Integer, primary_key=True)
    parent_id = Column(Integer, ForeignKey(id))
    name = Column(String(50), nullable=False)

    children = relationship(
        "TreeNode",
        # cascade deletions
        cascade="all, delete-orphan",
        # many to one + adjacency list - remote_side
        # is required to reference the 'remote'
        # column in the join condition.
        backref=backref("parent", remote_side=id),
        # children will be represented as a dictionary
        # on the "name" attribute.
        collection_class=attribute_mapped_collection("name"),
    )

    def __init__(self, name, parent=None):
        self.name = name
        self.parent = parent

    def __repr__(self):
        return "TreeNode(name=%r, id=%r, parent_id=%r)" % (
            self.name,
            self.id,
            self.parent_id,
        )

    def dump(self, _indent=0):
        return (
            "   " * _indent
            + repr(self)
            + "\n"
            + "".join([c.dump(_indent + 1) for c in self.children.values()])
        )


if __name__ == "__main__":
    engine = create_engine("sqlite://", echo=True)

    def msg(msg, *args):
        msg = msg % args
        print("\n\n\n" + "-" * len(msg.split("\n")[0]))
        print(msg)
        print("-" * len(msg.split("\n")[0]))

    msg("Creating Tree Table:")

    Base.metadata.create_all(engine)

    session = Session(engine)

    node = TreeNode("rootnode")
    TreeNode("node1", parent=node)
    TreeNode("node3", parent=node)

    node2 = TreeNode("node2")
    TreeNode("subnode1", parent=node2)
    node.children["node2"] = node2
    TreeNode("subnode2", parent=node.children["node2"])

    msg("Created new tree structure:\n%s", node.dump())

    msg("flush + commit:")

    session.add(node)
    session.commit()

    msg("Tree After Save:\n %s", node.dump())

    TreeNode("node4", parent=node)
    TreeNode("subnode3", parent=node.children["node4"])
    TreeNode("subnode4", parent=node.children["node4"])
    TreeNode("subsubnode1", parent=node.children["node4"].children["subnode3"])

    # remove node1 from the parent, which will trigger a delete
    # via the delete-orphan cascade.
    del node.children["node1"]

    msg("Removed node1.  flush + commit:")
    session.commit()

    msg("Tree after save:\n %s", node.dump())

    msg(
        "Emptying out the session entirely, selecting tree on root, using "
        "eager loading to join four levels deep."
    )
    session.expunge_all()
    node = (
        session.query(TreeNode)
        .options(
            joinedload_all("children", "children", "children", "children")
        )
        .filter(TreeNode.name == "rootnode")
        .first()
    )

    msg("Full Tree:\n%s", node.dump())

    msg("Marking root node as deleted, flush + commit:")

    session.delete(node)
    session.commit()
