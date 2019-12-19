# -*- coding: utf-8 -*-

import datetime
import logging

from chcko.db import *
from chcko.util import PageBase


class Page(PageBase):

    def __init__(self, _request):
        super().__init__(_request)
        self.assign_table = lambda: db.assign_table(
            self.request.student, self.user)

    def get_response(self):
        db.clear_done_assignments(self.request.student, self.user)
        return super().get_response()

    def post_response(self):
        for studentID in self.request.get_all('assignee'):
            db.assign_to_student(studentID,
                              self.request.get('query_string'),
                              self.request.get('duedays'))
        return self.get_response()
