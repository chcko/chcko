# -*- coding: utf-8 -*-

from chcko.util import PageBase
from chcko.db import db

class Page(PageBase):

    def post_response(self):
        email = self.request.forms.get('email','')
        password = self.request.forms.get('password','')
        if not (email and password):
            self.redirect('message?msg=f')
        self.request.user = db.user_by_login(email,password)
        self.renew_token()
        db.set_student(self.request,self.response)
        self.redirect('todo')

