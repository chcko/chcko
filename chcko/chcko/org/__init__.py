# -*- coding: utf-8 -*-

from chcko.chcko.util import PageBase
from chcko.chcko.db import db

class Page(PageBase):

    def post_response(self):
        choice = self.request.forms.get('choice','')
        oldpath = [self.request.forms.get('old' + x,'') for x in db.pathlevels]
        newpath = [self.request.forms.get(x,'') for x in db.pathlevels]
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
                db.delete_keys([oldstudent.key])
                # no student any more, redirect to get/generate a new one
                if choice == '1':  # change
                    self.redirect(
                        f'message?msg=h&oldname={oldname}&newname={newname}')
                elif choice == '2':  # delete
                    self.redirect(f'message?msg=g&studentname={oldname}')
        return self.get_response()
