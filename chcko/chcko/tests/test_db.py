import pytest
from chcko.chcko.tests.boddle import clear_all_data

@pytest.fixture()
def cdb(db):
    with db.dbclient.context():
        clear_all_data(db)
    with db.dbclient.context():
        yield db

@pytest.fixture()
def Student12345(cdb):
    s=cdb.School.get_or_insert("1")
    cdb.save(s)
    mkent = lambda t,i,o: t.get_or_insert(i,parent=o.key)
    p=mkent(cdb.Field,"2",s)
    cdb.save(p)
    t=mkent(cdb.Teacher,"3",p)
    cdb.save(t)
    c=mkent(cdb.Class,"4",t)
    cdb.save(c)
    st=mkent(cdb.Role,"5",c)
    cdb.save(st)
    return st

def test_key(cdb):
    k = cdb.Key('School', '1', 'Field', '2', 'Teacher', '3', 'Class', '4', 'Role', '5')
    assert k.pairs()==(('School', '1'), ('Field', '2'), ('Teacher', '3'), ('Class', '4'), ('Role', '5'))
    assert len(cdb.urlsafe(k)) > 30
    assert k.string_id()=="5"
    assert k.kind()=='Role'

def test_skey(Student12345):
    kk=Student12345.key
    assert kk.pairs()==(('School', '1'), ('Field', '2'), ('Teacher', '3'), ('Class', '4'), ('Role', '5'))
    assert kk.get().key.string_id()=="5"
    assert kk.kind()=="Role"
    assert kk.parent().pairs()==(('School', '1'), ('Field', '2'), ('Teacher', '3'), ('Class', '4'))
    assert kk.parent().get().key.string_id()=="4"

def test_get_or_insert(cdb):
    ut1=cdb.UserToken.get_or_insert(
        name="tokn"
        ,email="email1"
    )
    ut2=cdb.UserToken.get_or_insert(
        name="tokn"
        ,email="email1"
    )
    assert ut2.key==ut1.key

def test_token(cdb):
    token = cdb.token_create('email1')
    assert len(token)>10

def test_user(cdb):
    u1,_ = cdb.user_login('email2',fullname='fn',password='password2')
    u2,_ = cdb.user_login('email2',password='password2')
    assert u1.key == u2.key

def test_problem(cdb,Student12345):
    p = cdb.problem_create(Student12345,id='someid1',given=dict(zip('abc','ABC')),inputids=list('abc'),results=list('ABC'))
    cdb.save(p)
    us = p.key.urlsafe()
    problem = cdb.Key(urlsafe=us).get()
    problem.oks = [True,False,True]
    problem.points=[2]*3
    problem.answers=['1','','1']
    cdb.save(problem)
    np = cdb.Key(urlsafe=us).get()
    assert np.oks == [True,False,True]

