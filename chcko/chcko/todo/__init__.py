# -*- coding: utf-8 -*-

import datetime

from chcko.chcko.db import db
from chcko.chcko.util import PageBase


class Page(PageBase):

    def __init__(self, mod):
        super().__init__(mod)
        self.assign_table = lambda: db.assign_table(
            self.request.student, self.request.user)

    def get_response(self):
        db.clear_done_assignments(self.request.student, self.request.user)
        return super().get_response()

    def post_response(self):
        for studentkeyurlsafe in self.request.forms.getall('assignee'):
            db.assign_to_student(studentkeyurlsafe,
                              self.request.forms.get('query_string'),
                              self.request.forms.get('duedays'))
        return self.get_response()
