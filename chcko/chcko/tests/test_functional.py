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
    ,'/de/content?r.b'
    ,'/en/content/?r.a=2&r.b=3'
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

    def test_default_lang(self,chapp):
        r = chapp.get('/')
        assert r.status == '200 OK'
        assert 'problems' in r #engish index page

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
        #r = chapp.get('/en/?wrong', status=200)
        #assert '404' in r.status
        r = chapp.get('/en/?wrong')
        assert r.status == '200 OK'

    def test_register(self,chapp):
        self._signup(chapp)
        #'message?msg=j' then email with link to verification
        # this is skipped via
        assert '/verification' in self.resp.request.url

    def test_logout(self):
        r = self.resp.goto('/en/logout')
        self._store('resp', r.follow())
        assert 'log in' in self.resp
        # self.resp.showbrowser()

    def test_registersame(self,chapp):
        self._signup(chapp,pw='different')
        assert 'msg=a' in self.resp.request.url

    def test_anonymous(self):
        self._store('resp', self.resp.goto('/en/edits'))
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

    def test_edits(self):
        cur = self.resp.lxml
        curx = cur.xpath('//div[contains(text(),"School")]/text()')
        self._store('curs', curx[1].strip())
        self._store('resp', self.resp.goto('/en/edits'))
        for p in problemplaces[:-1]:
            self.resp.form[p] = 'tst'
        self.resp.form[problemplaces[-2]] = 'U' #U belongs to teacher/class=tst/tst
        self.resp.form['color'] = '#BBB'
        self._store('resp', self.resp.form.submit())
        assert 'edits' in self.resp.request.url
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
        tds = cur.xpath('//td[contains(text(),"tst")]/text()')
        assert len(tds) == 1
        trs = cur.xpath('//tr')
        assert len(trs) == 6

    def test_roles(self):
        self._store('resp', self.resp.goto('/en/roles'))
        cur = self.resp.lxml
        curx = cur.xpath('//div[contains(text(),"School")]//text()')
        assert curx[1].strip() != self.curs
        curh = cur.xpath('//a[contains(text(),"'+self.curs+'") and contains(@href,"todo")]/@href')[0]
        self._store('resp', self.resp.goto(curh))
        cur = self.resp.lxml
        curx = cur.xpath('//div[contains(text(),"School")]/text()')
        assert curx[1].strip() == self.curs
        # self.resp.showbrowser()

    def test_delete(self):
        self._store('resp', self.resp.goto('/en/edits'))
        self.resp.form['choice'] = '2'
        r = self.resp.form.submit()
        self._store('resp', r.follow())
        assert 'msg=g' in self.resp.request.url
        cur = self.resp.lxml
        curx = cur.xpath('//div[contains(text(),"School")]//text()')
        self._store('curs', curx[-1].strip())
        assert self.curs == 'tst'

    def test_change_color(self):
        self._store('resp', self.resp.goto('/en/edits'))
        self.resp.form['choice'] = '1'
        self.resp.form['color'] = '#CDE'  # only color
        self._store('resp', self.resp.form.submit())
        assert 'edits' in self.resp.request.url
        assert '#CDE' in self.resp
        # self.resp.showbrowser()

    def test_change_path(self):
        self._store('resp', self.resp.goto('/en/edits'))
        self.resp.form['Teacher'] = self.resp.form['Teacher'].value + 'x'
        self.resp.form['choice'] = '1'
        r = self.resp.form.submit()
        self._store('resp', r.follow())
        assert 'msg=h' in self.resp.request.url

    def test_assign(self):
        self._store('resp', self.resp.goto('/en/content'))
        assert "problems" in self.resp
        curx = self.resp.lxml
        probs = curx.xpath('//a[contains(@href,"en/content?r.b")]/@href')
        assert probs
        for prob in probs:
            #prob = '/en/content?r.bu'
            self._store('resp', self.resp.goto(prob))
            if len(self.resp.forms) > 1:
                form = self.resp.forms[1]  # assign
                assignees = form.fields.get('assignee')
                if assignees:
                    for a in assignees:
                        a.checked = True
                    res = form.submit('assign')
                    assert 'todo' in res.request.url

    def test_todo(self):
        self._store('resp', self.resp.goto('/en/todo'))
        curx = self.resp.lxml
        probs = curx.xpath('//a[contains(@href,"en/content?")]/@href')
        assert probs
        for prob in probs:
            #prob = '/en/content?r.bc'
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
        probs = curx.xpath('//a[contains(@href,"en/content?")]/@href')
        assert probs == []

    def test_done_delone(self):
        self._store('resp', self.resp.goto('/en/done'))
        # self.resp.showbrowser()
        curx = self.resp.lxml
        delone = curx.xpath('//a[contains(@href,"en/content?r.bb")]/../..//input')
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
        delone = curx.xpath('//a[contains(@href,"en/content?r.bb")]/../..//input')
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
        self._store(
            'rbuhref',
            curx.xpath('//a[contains(text(),"r.bu")]/@href')[0])
        self._store('resp', self.resp.goto(self.rbuhref))
        assert '0P' in self.resp

    def test_check_done_outside(self):
        r = self.resp.goto('/en/logout')
        self._store('resp', r.follow())
        self._store('resp', self.resp.goto(self.rbuhref))
        assert '0P' in self.resp
        # self.resp.showbrowser()

    def test_list_done_from_parent(self):
        self._store('resp', self.resp.goto('/en/done?tst&*&*'))
        curx = self.resp.lxml
        u_student = curx.xpath('//td[contains(text(),"tst")]/text()')
        assert len(u_student) == 4
