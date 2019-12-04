# -*- coding: utf-8 -*-

import datetime
import logging

from chcko.model import assigntable, table_entry, remove_done_assignments, assign_to_student
from chcko.util import PageBase


class Page(PageBase):

    def __init__(self, _request):
        super(self.__class__, self).__init__(_request)
        self.table = lambda: assigntable(
            self.request.student.key,
            self.user and self.user.key)
        self.params = {
            'table': self.table,
            'table_entry': table_entry}

    def get_response(self):
        remove_done_assignments(
            self.request.student.key,
            self.user and self.user.key)
        return super(self.__class__, self).get_response()

    def post_response(self):
        for urlsafe in self.request.get_all('assignee'):
            assign_to_student(urlsafe,
                              self.request.get('query_string'),
                              self.request.get('duedays'))
        return self.get_response()
