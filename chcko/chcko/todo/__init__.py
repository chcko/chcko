from chcko.chcko.db import db
from chcko.chcko.util import PageBase

class Page(PageBase):

    def __init__(self, mod):
        super().__init__(mod)
        self.assign_table = lambda: db.assign_table(
            self.request.student, self.request.user)

    def page_table(self):
        yield from db.depth_1st(*db.depth_1st_params(
            self.request.query_string
            , self.request.student.key
            , self.request.user and db.idof(self.request.user)
            , extraplace="Assignment"
                                ))

    def get_response(self,**kextra):
        db.clear_done_assignments(self.request.student, self.request.user)
        return super().get_response(**kextra)

    def post_response(self):
        for studentkeyurlsafe in self.request.forms.getall('assignee'):
            db.assign_to_student(studentkeyurlsafe,
                              self.request.forms.get('chuery'),
                              self.request.forms.get('duedays'))
        todelete = []
        for urlsafe in self.request.forms.getall('deletee'):
            todelete.append(db.Key(urlsafe=urlsafe))
        db.delete_keys(todelete)
        return self.get_response()
