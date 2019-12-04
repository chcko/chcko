# -*- coding: utf-8 -*-

from chcko.util import PageBase
from chcko.model import (
    Student,
    Problem,
    Assignment,
    studentCtx,
    delete_all,
    copy_all,
    ctxkey,
    keyparams)
import logging
from google.appengine.ext import ndb


class Page(PageBase):

    def post_response(self):
        choice = self.request.get('choice')
        oldpath = [self.request.get('old' + x) for x in studentCtx]
        newpath = [self.request.get(x) for x in studentCtx]
        pathchanged = not all([x[0] == x[1] for x in zip(oldpath, newpath)])
        if choice != '0':  # not new
            oldstudent = ctxkey(oldpath).get()
            if choice == '1' and pathchanged:  # change
                copy_all(Problem, oldstudent.key, self.request.student.key)
                copy_all(Assignment, oldstudent.key, self.request.student.key)
            if choice == '1' and pathchanged or choice == '2':  # delete
                delete_all(Problem.query(ancestor=oldstudent.key))
                delete_all(Assignment.query(ancestor=oldstudent.key))
                oldname = '/'.join([v for k, v in oldstudent.key.pairs()])
                newname = '/'.join([v for k,
                                    v in self.request.student.key.pairs()])
                oldstudent.key.delete()
                # no student any more, redirect to get/generate a new one
                if choice == '1':  # change
                    self.redirect(
                        "message?msg=h&oldname={}&newname={}".format(
                            oldname,
                            newname))
                elif choice == '2':  # delete
                    self.redirect(
                        "message?msg=g&studentname={}".format(oldname))
                return
        return self.get_response()
