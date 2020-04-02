# -*- coding: utf-8 -*-

import os
import re
import pytest
from webtest import TestApp as TA
from chcko.chcko import bottle
from chcko.chcko.languages import languages
from chcko.chcko.hlp import problemplaces
from chcko.chcko.tests.boddle import clear_all_data

@pytest.fixture(scope='module')
def chapp(request,db):
    with db.dbclient.context():
        clear_all_data(db)
    with db.dbclient.context():
        db.init_db()
    from chcko.chcko.app import app
    with db.dbclient.context():
        yield TA(app)

@pytest.mark.parametrize("path",[
    ''
    ,'/'
    ,'/en'
    ,'/de'
    ,'/en/?r.b'
    ,'/de?r.b'
    ,'/de/contents?r.b'
    ,'/en/contents/?r.a=2&r.b=3'
])
def test_paths(chapp,path):
    chapp.get(path)

# see
# https://stackoverflow.com/questions/12538808/pytest-2-3-adding-teardowns-within-the-class
# but cleanup is not necessary if testbed is in-memory

def url_lang(url):
    return re.match('http.*://localhost/([a-z]+)',url).group(1)

@pytest.mark.incremental
class TestRunthrough(object):

    resp = None

    @classmethod
    def _store(cls, name, value):
        setattr(cls, name, value)

    def _signup(self,chapp,pw=u'tpassword'):
        self._store('resp', chapp.get('/en/signup'))
        assert 'POST' == self.resp.form.method
        # self.resp.showbrowser()
        self.resp.form[u'email'] = u'temail@email.com'
        self.resp.form[u'password'] = pw
        self.resp.form[u'confirmp'] = pw
        self.resp.form[u'fullname'] = u'tfullname'
        r = self.resp.form.submit(expect_errors=True)
        self._store('resp', r.follow())

    def test_wrong_html(self,chapp):
        r = chapp.get('/ldkjfow.html',expect_errors=True)
        assert 'chcko' in r

    def test_wrong_image(self,chapp):
        r = chapp.get('/en/_images/jfj',expect_errors=True)
        assert 'chcko' in r
        r = chapp.get('/_images/jfj',expect_errors=True)
        assert 'chcko' in r
        r = chapp.get('/jfj.png',expect_errors=True)
        assert 'chcko' in r

    def test_default_lang(self,chapp):
        r = chapp.get('/')
        assert r.status == '200 OK'
        assert 'problems' in r #engish index page

    def test_with_param(self,chapp):
        r = chapp.get('?a=123.45&r.bu=2')
        assert '123.45' in r

    def test_wrong_lang(self,chapp):
        r = chapp.get('/wrong',expect_errors=True)
        assert '302' in r.status
        self._store('resp', r.follow())
        assert url_lang(self.resp.request.url) in languages

    def test_wrong_page(self,chapp):
        r = chapp.get('/en/wrong',expect_errors=True)
        assert '302' in r.status
        self._store('resp', r.follow())
        assert url_lang(self.resp.request.url) in languages

    def test_wrong_content(self,chapp):
        r = chapp.get('/en/?wrong')
        assert r.status == '200 OK'
        r = chapp.get('/en/?odufs.wew',expect_errors=True)
        assert 'chcko' in r
        r = chapp.get('/en/?erljy.woeur&odufs.wew',expect_errors=True)
        assert 'chcko' in r

    def test_wrong_done(self,chapp):
        r = chapp.get('/en/done/dfs',expect_errors=True)
        assert 'chcko' in r
        r = chapp.get('/en/done/*/',expect_errors=True)
        assert 'chcko' in r
        r = chapp.get('/en/done?kwuerlhg=9')
        assert 'chcko' in r

    def test_wrong_todo(self,chapp):
        r = chapp.get('/en/todo/dfs',expect_errors=True)
        assert 'chcko' in r
        r = chapp.get('/en/todo/*/',expect_errors=True)
        assert 'chcko' in r
        r = chapp.get('/en/todo?kwuerlhg=9')
        assert 'chcko' in r

    def test_register(self,chapp):
        self._signup(chapp)
        # 'message?msg=j' then email with link to verification
        assert '/verification' in self.resp.request.url
        self._store('usertoken', chapp.cookies.get('chcko_cookie_usertoken'))

    def test_logout(self):
        r = self.resp.goto('/en/logout')
        self._store('resp', r.follow())
        assert 'Login' in self.resp
        # self.resp.showbrowser()

    #def test_wrong_cookie(self,chapp):
    #    chapp.set_cookie('chcko_cookie_usertoken','A'*len(self.usertoken))
    #    r = chapp.get('/en')
    #    assert '200' in r.status
    #    del chapp.cookies['chcko_cookie_usertoken']

    def test_registersame(self,chapp):
        self._signup(chapp,pw='different')
        assert 'msg=a' in self.resp.request.url

    def test_anonymous(self):
        self._store('resp', self.resp.goto('/en/org'))
        for p in problemplaces[:-1]:
            self.resp.form[p] = 'tst'
        # later we will check access permission
        self._store('resp', self.resp.form.submit())

    def test_anonym_exercise(self):
        self._store('resp', self.resp.goto('/en/?r.bu'))
        self.resp.form[u'0000_0000'] = u'x'
        self._store('resp', self.resp.form.submit())
        assert '0P' in self.resp

    def test_forgot(self,chapp):
        self._store('resp', chapp.get('/en/forgot'))
        assert 'POST' == self.resp.form.method
        self.resp.form[u'email'] = u'temail@email.com'
        r = self.resp.form.submit()
        assert '302' in r.status
        r = r.follow()
        assert '302' in r.status
        self._store('resp', r.follow())
        assert 'POST' == self.resp.form.method
        self.resp.form[u'password'] = u'tpassword'
        self.resp.form[u'confirmp'] = u'tpassword'
        r = self.resp.form.submit()
        assert '302' in r.status
        self._store('resp', r.follow())
        # self.resp.showbrowser()
        assert 'msg=d' in self.resp.request.url

    def test_login(self,chapp):
        self._store('resp', chapp.get('/en/login'))
        assert 'POST' == self.resp.form.method
        # self.resp.showbrowser()
        self.resp.form[u'email'] = u'temail@email.com'
        self.resp.form[u'password'] = u'tpassword'
        r = self.resp.form.submit()
        self._store('resp', r.follow())
        # self.resp.showbrowser()
        assert '/todo' in self.resp.request.url
        assert 'Logout' in self.resp

    def test_password(self):
        self._store('resp', self.resp.goto('/en/password'))
        self.resp.form[u'password'] = u'tpassword'
        self.resp.form[u'confirmp'] = u'tpassword'
        r = self.resp.form.submit()
        self._store('resp', r.follow())
        assert 'msg=d' in self.resp.request.url

    def test_loginedwrong(self,chapp):
        r = chapp.get('/en/?fdsr.bdfsu',expect_errors=True)
        assert 'Logout' in r
        r = chapp.get('/en/done/*',expect_errors=True)
        assert 'Logout' in r
        r = chapp.get('/en/todo/*',expect_errors=True)
        assert 'Logout' in r

    def test_edits(self):
        cur = self.resp.lxml
        curx = cur.xpath('//div[contains(text(),"School")]//text()')
        curx = [x for x in curx if x.strip()]
        self._store('curs', curx[-1].strip())
        self._store('resp', self.resp.goto('/en/org'))
        for p in problemplaces[:-1]:
            self.resp.form[p] = 'tst'
        self.resp.form[problemplaces[-2]] = 'U' #U belongs to teacher/class=tst/tst
        self.resp.form['color'] = '#BBB'
        self._store('resp', self.resp.form.submit())
        assert 'org' in self.resp.request.url
        assert 'tst' in self.resp
        assert '#BBB' in self.resp

    def test_registered_exercise(self):
        self._store('resp', self.resp.goto('/en/?r.bu'))
        #only one form is expected,
        #because this student and the teacher have different users
        #(the teacher has no user. see test_anonymous above)
        form = self.resp.forms[0]
        form[u'0000_0000'] = u'x'
        self._store('resp', form.submit())
        assert '0P' in self.resp

    def test_no_permission(self):
        self._store('resp', self.resp.goto('/en/done?tst&*&*'))
        # tst does not belong to this user, therefore not listed
        cur = self.resp.lxml
        tds = cur.xpath('//td[contains(text(),"tst")]//text()')
        assert len(tds) == 1
        trs = cur.xpath('//tr')
        assert len(trs) == 6

    def test_delete(self):
        self._store('resp', self.resp.goto('/en/org?School=newster&Field=newster&Teacher=newster&Class=newster&Role=newster'))
        self.resp.form['choice'] = '2'
        r = self.resp.form.submit()
        self._store('resp', r.follow())
        assert 'msg=g' in self.resp.request.url
        cur = self.resp.lxml
        curx = [x for x in cur.xpath('//div[contains(text(),"School")]//text()') if x.strip()]
        self._store('curs', curx[-1].strip())
        assert self.curs != 'tst'

    def test_change_color(self):
        self._store('resp', self.resp.goto('/en/org?School=tst&Field=tst&Teacher=tst&Class=tst&Role=tst'))
        self.resp.form['choice'] = '1'
        self.resp.form['color'] = '#CDE'  # only color
        self._store('resp', self.resp.form.submit())
        assert 'org' in self.resp.request.url
        assert '#CDE' in self.resp
        # self.resp.showbrowser()

    def test_change_path(self):
        self._store('resp', self.resp.goto('/en/org'))
        self.resp.form['Teacher'] = self.resp.form['Teacher'].value + 'x'
        self.resp.form['choice'] = '1'
        r = self.resp.form.submit()
        self._store('resp', r.follow())
        assert 'msg=h' in self.resp.request.url

    def test_assign(self):
        self._store('resp', self.resp.goto('/en/contents'))
        assert "problems" in self.resp
        curx = self.resp.lxml
        probs = curx.xpath('//a[contains(@href,"en/contents?r.b")]/@href')
        assert probs
        for prob in probs:
            #prob = '/en/contents?r.bu'
            self._store('resp', self.resp.goto(prob))
            try:
                form = self.resp.forms[1]
            except:
                pass #non-problems cannot be assigned
            assignees = form.fields.get('assignee')
            if assignees:
                for a in assignees:
                    a.checked = True
                res = form.submit('assign')
                assert 'todo' in res.request.url

    def test_todo(self):
        self._store('resp', self.resp.goto('/en/todo'))
        curx = self.resp.lxml
        probs = curx.xpath('//a[contains(@href,"en/contents?")]/@href')
        assert probs
        for prob in probs:
            #prob = '/en/contents?r.bc'
            self._store('resp', self.resp.goto(prob))
            form = self.resp.forms[0]
            inps = form.fields.values()
            allnames = [i[0].name for i in inps]
            names = [n for n in allnames if n and re.match('\d+', n)]
            for n in names:
                # n=names[3]
                inp = form[n]
                if inp.attrs['type'] == 'text':
                    form[n] = '1.,-'
                else:
                    form[n] = '1'
            if 'submit' in allnames:
                res = form.submit('submit')
                assert "Assign" in res
                assert "Check" not in res
        self._store('resp', self.resp.goto('/en/todo'))
        curx = self.resp.lxml
        probs = [x for x in curx.xpath('//a[contains(@href,"en/contents?")]/@href') if 'School' not in x]
        assert probs == []

    def test_done_delone(self):
        self._store('resp', self.resp.goto('/en/done'))
        # self.resp.showbrowser()
        curx = self.resp.lxml
        delone = curx.xpath('//a[contains(@href,"en/contents?r.bb")]/../..//input')
        value = ''
        if 'value' in delone[0].keys():
            value = dict(delone[0].items())['value']
        if value:
            form = self.resp.form
            deletees = form.fields.get('deletee')
            d = [d for d in deletees if d._value == value]
            if d:
                d = d[0]
                d.checked = True
        self._store('resp', form.submit('submit'))
        curx = self.resp.lxml
        delone = curx.xpath('//a[contains(@href,"en/contents?r.bb")]/../..//input')
        assert delone == []  # deleted

    def test_done_delall(self):
        self._store('resp', self.resp.goto('/en/done'))
        form = self.resp.form
        deletees = form.fields.get('deletee')
        for d in deletees:
            d.checked = True
        self._store('resp', form.submit('submit'))
        form = self.resp.form
        assert None == form.fields.get('deletee')

    def test_access_to_other_exercise(self):
        self._store('resp', self.resp.goto('/en/?r.bu'))
        self.resp.forms[0][u'0000_0000'] = u'x'
        self._store('resp', self.resp.forms[0].submit())
        assert '0P' in self.resp

    def test_check_done(self):
        self._store('resp', self.resp.goto('/en/done'))
        curx = self.resp.lxml
        self._store('rbuhref',curx.xpath('//a[contains(text(),"r.bu")]/@href')[0])
        self._store('resp', self.resp.goto(self.rbuhref))
        assert '0P' in self.resp
        u_student = [x for x in curx.xpath('//div//text()') if 'tst' in x]
        assert len(u_student) > 0

    def test_check_done_outside(self):
        r = self.resp.goto('/en/logout')
        self._store('resp', r.follow())
        self._store('resp', self.resp.goto(self.rbuhref, expect_errors=True))
        assert 'No Access 6' in self.resp
        # self.resp.showbrowser()

    def test_list_done_from_parent(self):
        self._store('resp', self.resp.goto('/en/done?tst&*&*'))
        curx = self.resp.lxml
        u_student = [x for x in curx.xpath('//div/text()') if 'tst' in x]
        assert len(u_student) == 0
