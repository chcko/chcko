from chcko.chcko.db import db
from chcko.chcko.util import PageBase

class Page(PageBase):

    def page_table(self):
        yield from db.depth_1st(*db.depth_1st_params(
            self.request.query_string
            , self.request.student.key
            , self.request.user and db.idof(self.request.user)
            ))

    def post_response(self):
        todelete = []
        for urlsafe in self.request.forms.getall('deletee'):
            todelete.append(db.Key(urlsafe=urlsafe))
        db.delete_keys(todelete)
        return self.get_response()
