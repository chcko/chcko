
''' TODO
p = db.problem_create(id='someid1',inputids=list('abc'),
        oks=[True,False,True],points=[2]*3,answers=['1','','1'])
f = lambda c:c
withempty,noempty = Page.make_summary(p)
sfmt = u"{oks}/{of}->{points}/{allpoints}"
sfmt.format(**withempty)+u"  no empty:" + sfmt.format(**noempty)
u'2/3->4/6  no empty:2/2->4/4'

'''

import pytest

@pytest.fixture()
def cdb(db):
    db.clear_all_data()
    return db

@pytest.fixture()
def Student12345(cdb):
    s=cdb.School.get_or_insert("1")
    s.put()
    mkent = lambda t,i,o: t.get_or_insert(i,parent=o.key)
    p=mkent(cdb.Period,"2",s)
    p.put()
    t=mkent(cdb.Teacher,"3",p)
    t.put()
    c=mkent(cdb.Class,"4",t)
    c.put()
    st=mkent(cdb.Student,"5",c)
    st.put()
    return st

def test_key(cdb):
    k = cdb.Key('School', '1', 'Period', '2', 'Teacher', '3', 'Class', '4', 'Student', '5')
    assert k.pairs()==(('School', '1'), ('Period', '2'), ('Teacher', '3'), ('Class', '4'), ('Student', '5'))
    assert len(k.urlsafe()) > 30
    assert k.string_id()=="5"
    assert k.kind()=='Student'

def test_skey(Student12345):
    kk=Student12345.key
    assert kk.pairs()==(('School', '1'), ('Period', '2'), ('Teacher', '3'), ('Class', '4'), ('Student', '5'))
    assert kk.get().key.string_id()=="5"
    assert kk.kind()=="Student"
    assert kk.parent().pairs()==(('School', '1'), ('Period', '2'), ('Teacher', '3'), ('Class', '4'))
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
    u1= cdb.user_create('email2','password2','fn')
    u2 = cdb.user_by_login('email2','password2')
    assert u1.key == u2.key
