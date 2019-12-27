# -*- coding: utf-8 -*-

from chcko.util import PageBase
from chcko.db import db

class Page(PageBase):

    def post_response(self):
        choice = self.request.forms.get('choice','')
        oldpath = [self.request.forms.get('old' + x,'') for x in db.student_contexts]
        newpath = [self.request.forms.get(x,'') for x in db.student_contexts]
        pathchanged = not all([x[0] == x[1] for x in zip(oldpath, newpath)])
        if choice != '0':  # not new
            oldstudent = db.key_from_path(oldpath).get()
            if choice == '1' and pathchanged:  # change
                db.copy_to_new_student(oldstudent,self.request.student)
            if choice == '1' and pathchanged or choice == '2':  # delete
                db.clear_student_problems(oldstudent)
                db.clear_student_assignments(oldstudent)
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
