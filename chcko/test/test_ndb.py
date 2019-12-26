import pytest

@pytest.fixture(scope="module")
def db():
    from chcko import ndb
    adb = ndb.Ndb()
    with adb.dbclient.context():
        yield adb

@pytest.fixture()
def Student12345(db):
    s=db.School(id="1")
    s.put()
    mkent = lambda t,i,o: t(id=i,parent=o.key)
    p=mkent(db.Period,"2",s)
    p.put()
    t=mkent(db.Teacher,"3",p)
    t.put()
    c=mkent(db.Class,"4",t)
    c.put()
    st=mkent(db.Student,"5",c)
    st.put()
    return st

def test_key(db):
    k = db.Key('School', '1', 'Period', '2', 'Teacher', '3', 'Class', '4', 'Student', '5')
    assert k.pairs()==(('School', '1'), ('Period', '2'), ('Teacher', '3'), ('Class', '4'), ('Student', '5'))
    assert len(k.urlsafe()) > 30
    assert k.string_id()=="5"
    assert k.kind()=='Student'

def test_skey(db,Student12345):
    kk=Student12345.key
    assert kk.pairs()==(('School', '1'), ('Period', '2'), ('Teacher', '3'), ('Class', '4'), ('Student', '5'))
    assert kk.get().key.string_id()=="5"
    assert kk.kind()=="Student"
    assert kk.parent().pairs()==(('School', '1'), ('Period', '2'), ('Teacher', '3'), ('Class', '4'))
    assert kk.parent().get().key.string_id()=="4"

def test_ut(db):
    ut1=db.UserToken.get_or_insert(
        "1"
        ,subject="signup"
        ,email="email1"
        ,token="tokn"
    )
    ut2=db.UserToken.get_or_insert(
        "1"
        ,subject="signup"
        ,email="email1"
        ,token="tokn"
    )
    assert ut2.key==ut1.key

def test_token(db):
    ut = db.UserToken.create('email1','signup')
    assert len(ut.token)>10

def test_user(db):
    u = db.User.create('email1','password1')
    u1 = db.User.by_login('email1','password1')
    assert u.key == u1.key

