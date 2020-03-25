# -*- coding: utf-8 -*-

import datetime

from chcko.chcko.db import db
from chcko.chcko.util import PageBase

from chcko.chcko.done import prepare


class Page(PageBase):

    def __init__(self, mod):
        super().__init__(mod)
        self.assign_table = lambda: db.assign_table(
            self.request.student, self.request.user)

    def page_table(self):
        qs = self.request.query_string
        skey = self.request.student.key
        userkey = self.request.user and db.idof(self.request.user)
        yield from db.depth_1st(*prepare(qs,skey,userkey,extraplace="Assignment"))

    def get_response(self):
        db.clear_done_assignments(self.request.student, self.request.user)
        return super().get_response()

    def post_response(self):
        for studentkeyurlsafe in self.request.forms.getall('assignee'):
            db.assign_to_student(studentkeyurlsafe,
                              self.request.forms.get('query_string'),
                              self.request.forms.get('duedays'))
        todelete = []
        for urlsafe in self.request.forms.getall('deletee'):
            todelete.append(db.Key(urlsafe=urlsafe))
        db.delete_keys(todelete)
        return self.get_response()
