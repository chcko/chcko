# -*- coding: utf-8 -*-
'''
This file contains functions and classes doing datastore access,
especially the models.

'''

import datetime
import uuid
import time
from itertools import chain
from bottle import SimpleTemplate
from urllib.parse import parse_qsl

from chcko.hlp import int_to_base26, datefmt
from chcko.languages import langkindnum, langnumkind, kindint

from google.cloud import ndb

def delete_all(query):
    'delete_all(entity.query(entity.field==value))'
    ndb.delete_multi(query.iter(keys_only=True))

def copy_all(model, oldkey, newkey):
    '''copy all instances of a model from an old parent to a new one'''
    computed = [
        k for k,
        v in model._properties.iteritems() if isinstance(
            v, ndb.ComputedProperty)]
    for entry in model.query(ancestor=oldkey).iter():
        cpy = model(id=entry.key.string_id(), parent=newkey)
        cpy.populate(
            **{k: v for k, v in entry.to_dict().items() if k not in computed})
        cpy.put()


import hashlib
from hmac import compare_digest
from random import choice
METHOD = "pbkdf2:sha256:150000"
SALT_CHARS = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
def gen_salt():
    """
    >>> gen_salt()
    """
    return "".join(choice(SALT_CHARS) for _ in range(22))

def generate_password_hash(password):
    """
    >>> generate_password_hash('xy')
    pbkdf2:sha256:150000$hTYkIQcs$f5fe71456afb70fff81dca8647fa57a443e89f5b83a28ecfaeeb3144aa489dc1
    """
    salt = gen_salt()
    h = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt.encode("utf-8"), 150000).hex()
    return "%s$%s$%s" % (METHOD, salt, h)

def check_password_hash(pwhash, password):
    """
    >>> pwhash = "pbkdf2:sha256:150000$hTYkIQcs$f5fe71456afb70fff81dca8647fa57a443e89f5b83a28ecfaeeb3144aa489dc1"
    >>> password = 'xy'
    >>> check_password_hash(pwhash, 'xy')
    """
    if pwhash.count("$") < 2:
        return False
    method, salt, hashval = pwhash.split("$", 2)
    if method != METHOD:
        return False
    h = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt.encode("utf-8") , 150000).hex()
    equal = compare_digest(h,hashval)
    return equal

class UserToken(ndb.Model):
    created = ndb.DateTimeProperty(auto_now_add=True)
    updated = ndb.DateTimeProperty(auto_now=True)
    user = ndb.StringProperty(required=True)
    subject = ndb.StringProperty(required=True)
    token = ndb.StringProperty(required=True)
    @classmethod
    def get_key(cls, user, subject, token):
        return model.Key(cls, '%s.%s.%s' % (str(user), subject, token))
    @classmethod
    def create(cls, user, subject, token=None):
        user = str(user)
        token = token or gen_salt()
        key = cls.get_key(user, subject, token)
        entity = cls(key=key, user=user, subject=subject, token=token)
        entity.put()
        return entity
    @classmethod
    def get(cls, user=None, subject=None, token=None):
        if user and subject and token:
            return cls.get_key(user, subject, token).get()
        assert subject and token, \
            'subject and token must be provided to UserToken.get().'
        return cls.query(cls.subject == subject, cls.token == token).get()

class User(ndb.User):
    current_student = ndb.KeyProperty(kind='Student')
    token_model = ndb.StructuredProperty(UserToken)
    def set_password(self, password):
        self.password = generate_password_hash(password)
    @classmethod
    def get_by_auth_token(cls, user_id, token, subject='auth'):
        token_key = cls.token_model.get_key(user_id, subject, token)
        user_key = ndb.Key(cls, user_id)
        valid_token, user = ndb.get_multi([token_key, user_key])
        if valid_token and user:
            timestamp = int(time.mktime(valid_token.created.timetuple()))
            return user, timestamp
        return None, None

class Secret(ndb.Model):  # root
    '''this is filled manually with (TODO check)::

        $remote_api_shell.py -s chcko.appspot.com
    '''
    secret = ndb.StringProperty()

def make_secret():
    '''
    >>> make_secret()
    '''
    asecret = str(uuid.uuid5(
    uuid.UUID(bytes=datetime.datetime.now().isoformat()[:16].encode()),
    datetime.datetime.now().isoformat()))
    return asecret

def stored_secret(name):
    '''
    >>> name = 'xyz'
    >>> stored_secret(name)
    '''
    ass = str(
        Secret.get_or_insert(
        name,
        secret=make_secret()).secret)
    return ass

def gen_student_path(seed=None):
    ''' used if no federated user id
    >>> #myschool,myperiod,myteacher,myclass,myself = gen_student_path().split('-')
    '''
    if not seed:
        seed = datetime.datetime.now().isoformat()
    while len(seed) < 16:
        seed = seed + datetime.datetime.now().isoformat().split(':')[-1]
    student_path = str(
        uuid.uuid5(
            uuid.UUID(
                bytes=seed[
                    :16]),
            datetime.datetime.now().isoformat()))
    return student_path


class Base(ndb.Model):  # root
    'common fields'
    userkey = ndb.KeyProperty(kind='User')
    created = ndb.DateTimeProperty(auto_now_add=True)


# these are roles
# a user can have more such roles

class School(Base):
    'root'
    pass


class Period(Base):
    'parent:School'
    pass


class Teacher(Base):
    'parent:Period'
    pass


class Class(Base):
    'parent: Teacher'
    pass


class Student(Base):
    'parent: Class'
    color = ndb.StringProperty()

#os.environ['DATASTORE_EMULATOR_HOST']='localhost:8081'
db = ndb.Client('chcko')
with db.context():
    myschool = School.get_or_insert('myschool')
    myperiod = Period.get_or_insert('myperiod', parent=myschool.key)
    myteacher = Teacher.get_or_insert('myteacher', parent=myperiod.key)
    myclass = Class.get_or_insert('myclass', parent=myteacher.key)
    myself = Student.get_or_insert('myself', parent=myclass.key)

def add_student(studentpath, color=None, user=None):
    'defaults to myxxx for empty roles'
    school_, period_, teacher_, class_, student_ = studentpath
    school = School.get_or_insert(
        school_ or 'myschool',
        userkey=user and user.key)
    period = Period.get_or_insert(
        period_ or 'myperiod',
        parent=school.key,
        userkey=user and user.key)
    teacher = Teacher.get_or_insert(
        teacher_ or 'myteacher',
        parent=period.key,
        userkey=user and user.key)
    clss = Class.get_or_insert(
        class_ or 'myclass',
        parent=teacher.key,
        userkey=user and user.key)
    self = Student.get_or_insert(
        student_ or 'myself',
        parent=clss.key,
        userkey=user and user.key,
        color=color or '#EEE')
    if self.userkey == (user and user.key) and (color and self.color != color):
        self.color = color
        self.put()
    return self

#dict(filter(lambda x:isinstance(x[1],ndb.ComputedProperty),Problem._properties.iteritems()))


class Problem(Base):
    'parent: Student'
    query_string = ndb.StringProperty()
    lang = ndb.StringProperty()
    # the numbers randomly chosen, in python dict format
    given = ndb.PickleProperty()
    created = ndb.DateTimeProperty(auto_now_add=True)
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
    allempty = ndb.ComputedProperty(lambda self: ''.join(self.answers) == '')

    def link(self):
        'creates url to this problem'
        return '/' + self.lang + '/?' + self.query_string

    @classmethod
    def from_resolver(cls, rsv, nr, parentkey):
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
        problem = cls(parent=parentkey,
                      **{s: pkwargs[s] for s,
                         v in cls._properties.items() if s in pkwargs})
        return problem, pkwargs


def keyparams(k):
    '''
    >>> e=myself.key
    >>> keyparams(e)
    'School=myschool&Period=myperiod&Teacher=myteacher&Class=myclass&Student=myself'

    '''
    return '&'.join([r + '=' + str(v) for r, v in k.pairs()])


def ctxkey(x):
    '''
    >>> x = ['myschool','myperiod','myteacher','myclass','myself']
    >>> isinstance(ctxkey(x),ndb.Key)
    True

    '''
    return ndb.Key(*list(chain(*zip(problemCtx[:len(x)], x))))


studentCtx = [k for k, v in myself.key.pairs()]
problemCtx = studentCtx + ['Problem']
problemCtxObjs = [School, Period, Teacher, Class, Student, Problem]

def table_entry(e):
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


class Index(ndb.Model):
    '''holds the index of the content.

    entity name = <query id>:<lang>, like 'r.i:de'
    This way it becomes unique in the Index table.
    '''
    path = ndb.StringProperty()
    knd = ndb.IntegerProperty()
    level = ndb.IntegerProperty()


def index_add(query, lang, kind, level, path):
    '''used in the generated initdb.py to fill the index (see dodo.py)
    >>> index_add("r.bw", "en", "0", "11","maths/finance/interest/combined and theoretical")
    '''
    Index.get_or_insert(
        query + ':' + lang,
        knd=int(kind),
        level=int(level),
        path=path)

def kvld(p_ll):  # key_value_leaf_depth
    '''
    >>> p_ll = [('a/b','ab'),('n/b','nb'),('A/c','ac')]
    >>> [(a,d) for a, b, c, d in list(kvld(p_ll))]
    [('a', '1a'), ('b', '2a'), ('c', '2b'), ('n', '1b'), ('b', '2a')]

    '''
    previous = []
    depths = []
    for p, ll in sorted(p_ll, key=lambda v:v[0].lower()):
        keypath = p.split('/')
        this = []
        nkeys = len(keypath)
        for depth, kk in enumerate(keypath):
            if depth >= len(depths):
                depths.append(0)
            this.append(kk)
            if [x.lower() for x in this] < [x.lower() for x in previous]:
                continue
            else:
                del depths[depth+1:]
                lvl_idx = str(depth + 1) + int_to_base26(depths[depth])
                depths[depth] = depths[depth] + 1
                yield (kk, ll, depth == nkeys - 1, lvl_idx)
                previous = this[:]


def filteredcontent(lang, opt):
    ''' filters the index by lang and optional by

        - level
        - kind
        - path
        - link

    >>> from chcko import initdb
    >>> lang = 'en'
    >>> opt1 = [] #[('level', '2'), ('kind', 'exercise')]
    >>> cnt1 = sum([len(list(gen[1])) for gen in filteredcontent(lang, opt1)])
    >>> opt2 = [('level', '10'),('kind','1'),('path','maths'),('link','r')]
    >>> cnt2 = sum([len(list(gen[1])) for gen in filteredcontent(lang, opt2)])
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
    knd_pl = [(numkind[k], kvld(v)) for k, v in s_pl]
    #[('Problems', <generator>), ('Content', <generator>),... ]
    return knd_pl


def keysOmit(path):
    "[name1,name2,nonstr,...]->[key2,key2]"
    keys = []
    pth = [isinstance(x, str) for x in path]
    ipth = pth.index(False) if False in pth else len(pth)
    if ipth > 0:
        keys = [ctxkey(path[:ipth])] * ipth
    return keys

# pylint: disable=W0102
def depth_1st(path=None, keys=None  # start keys, keysOmit(path) to skip initial hierarchy
              , models=problemCtxObjs
              , permission=False, userkey=None
              ):
    ''' path entries are names or filters ([] for all)
    translated into keys along the levels given by **models** depth-1st-wise.

    >>> from chcko.test.hlp import problems_for
    >>> #del sys.modules['chcko.test.hlp']
    >>> path = ['a', 'b', 'c', 'd', 'e']
    >>> student = add_student(path, 'EEE')
    >>> problems_for(student)
    >>> lst = list(depth_1st(path+[[]]))
    >>> [k.get() for k in list(depth_1st(path+[[('query_string','=','r.u')]]))][0]._get_kind()
    'School'
    >>> path = ['a', 'b', 'c', 'x', 'e']
    >>> student1 = add_student(path, 'EEE')
    >>> problems_for(student1)
    >>> path = ['a','b','c',[],[],[('query_string','=','r.u')]]
    >>> list(depth_1st(path))[0].kind()
    'School'
    >>> list(depth_1st(path,keys=keysOmit(path)))[0].kind()
    'Class'
    >>> list(depth_1st())
    []

    '''
    N = len(models)
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
        k = ndb.Key(models[i]._get_kind(), path[i], parent=parentkey)
        if k:
            yield k
            if i < N - 1:
                keys.append(k)
                for e in depth_1st(path, keys, models, permission, userkey):
                    yield e
                del keys[-1]
    elif permission:
        q = models[i].query(ancestor=parentkey)
        #q = Assignment.query(ancestor=studentkey)
        if models[i] == Problem:
            q = q.order(Problem.answered)
        elif 'created' in models[i]._properties:
            q = q.order(models[i].created)
        for ap, op, av in path[i]:
            if ap in models[i]._properties:
                fn = ndb.FilterNode(ap, op, av)
                q = q.filter(fn)
        #qiter = q.iter(keys_only=True)
        for k in q.iter(keys_only=True):
            # k=next(qiter)
            yield k
            if i < N - 1:
                keys.append(k)
                for e in depth_1st(path, keys, models, permission):
                    yield e
                del keys[-1]
    # else:
    # yield None #no permission or no such object


def filter_student(qs):
    '''take out studentCtx and color
    >>> qs = 'School=b&Period=3&Teacher=5e&Class=9&Student=0&color=#E&bm&ws>0,d~1&b.v=3'
    >>> filter_student(qs)
    'bm&ws>0,d~1&b.v=3'

    '''
    qfiltered = [x  for x in
            parse_qsl(qs, True)
            if x[0] not in studentCtx + ['color']]
    qsfiltered = '&'.join([k + '=' + v if v else k for k, v in qfiltered])
    return qsfiltered


def set_student(request, user=None, session=None):
    '''logic for student role

    There is always a student role

    - there is a student role per client without user
    - there are more student roles for a user with one being current

    Else a redirect string for a message is returned.

    >>> import webapp2
    >>> request = webapp2.Request.blank('/')
    >>> request.response = request.get_response()
    >>> request.GET.update(dict(zip(studentCtx,[str(x) for x in range(len(studentCtx))])))
    >>> st=set_student(request)
    >>> request.student.key is not None
    True
    >>> #request.student.key.flat()

    '''
    request.student = None
    studentpath = [request.get(x) for x in studentCtx]
    color = request.get('color')
    request.query_string = filter_student(request.query_string)
    studentwithoutuser = 'studentwithoutuser'
    if ''.join(studentpath) != '':
        student = add_student(studentpath, color, user)
        if student.userkey == (user and user.key):
            request.student = student
        # student role does not belong to user, so don't change current student
        else:
            return 'message?msg=e'
    elif user:
        request.student = user.current_student and user.current_student.get()
    elif session is not None and studentwithoutuser in session:
        try:
            request.student = ndb.Key(
                urlsafe=session[studentwithoutuser]).get()
        except (TypeError, BadKeyError, AttributeError):
            pass  # no valid cookie available
    if not request.student and user:
        request.student = Student.query(Student.userkey == user.key).get()
    if not request.student:  # generate
        studentpath = gen_student_path(seed=request.remote_addr).split('-')
        request.student = add_student(studentpath, color, user)
    if user:
        if user.current_student != request.student.key:
            user.current_student = request.student.key
            user.put()
    elif session is not None:
        session[studentwithoutuser] = request.student.key.urlsafe()
    SimpleTemplate.defaults.update(dict(zip(problemCtx, problemCtxObjs)))
    SimpleTemplate.defaults["contextcolor"] = request.student.color or '#EEE'
    SimpleTemplate.defaults["keyparams"] = keyparams
    SimpleTemplate.defaults["ctxkey"] = ctxkey
    return request.student


class Assignment(Base):
    'parent: Student'
    query_string = ndb.StringProperty()
    due = ndb.DateTimeProperty()


def assignable(teacherkey, userkey):
    'yield all classes and students the teacher can assign to'
    for st in depth_1st(keys=[teacherkey], models=[Teacher, Class, Student], userkey=userkey):
        yield st


def normqs(qs):
    '''take away =1 from a content query

    >>> qs = 'r.bm=1'
    >>> normqs(qs)
    'r.bm'
    >>> qs = 'r.bm=2'
    >>> normqs(qs)
    'r.bm=2'
    >>> qs = 'r.bm'
    >>> normqs(qs)
    'r.bm'
    >>> qs = 'r.bm&r.x=1'
    >>> normqs(qs)
    'r.bm&r.x=1'

    '''
    qparsed = parse_qsl(qs, True)
    if len(qparsed) == 1 and qparsed[0][1] == '1':
        return qparsed[0][0]
    return qs


def assign_to_student(studentkeyurlsafe, query_string, duedays):
    'assign to a student'
    now = datetime.datetime.now()
    studentkey = ndb.Key(urlsafe=studentkeyurlsafe)
    Assignment(parent=studentkey, query_string=normqs(query_string),
               due=now + datetime.timedelta(days=int(duedays))).put()


def assigntable(studentkey, userkey):
    'yield assignment table for student'
    for e in depth_1st(keys=[studentkey], models=[Student, Assignment], userkey=userkey):
        yield e


def done_assignment(akey):
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


def remove_done_assignments(studentkey, userkey):
    'remove all done assignments for a student'
    for s in assigntable(studentkey, userkey):
        if done_assignment(s):
            s.delete()


#email
import base64
import pickle
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from email.mime.text import MIMEText
mail_id='chcko.mail@gmail.com'
pth = lambda x: os.path.join(os.path.dirname(__file__),x)
credential_file = pth('credentials.json')
token_file = pth('token.pickle')
def get_credential():
    creds = None
    if os.path.exists(token_file):
        with open(token_file, 'rb') as tokenf:
            creds = pickle.load(tokenf)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
              pth(credential_file)
              ,['https://www.googleapis.com/auth/gmail.send'])
            creds = flow.run_local_server(port=0)
        with open(token_file, 'wb') as tokenf:
            pickle.dump(creds, tokenf)
    return creds
def send_mail(sender, to, subject, message_text):
    '''
    >>> (sender, to, subject, message_text) = (mail_id,'roland.puntaier@gmail.com','test 2','test second message text')
    >>> send_mail(sender, to, subject, message_text)
    '''
    creds = None
    if not is_standard_server:
        creds = get_credential()
    else:
        # token placed there manually via console.google.cloud
        creds = base64.urlsafe_b64decode(stored_secret('chcko.mail').encode())
    service = build('gmail', 'v1', credentials=creds)
    message = MIMEText(message_text)
    message['to'] = to
    message['from'] = sender
    message['subject'] = subject
    mbody = {'raw':base64.urlsafe_b64encode(message.as_bytes()).decode()}
    message = (service.users().messages().send(userId=mail_id, body=mbody).execute())
    return message
