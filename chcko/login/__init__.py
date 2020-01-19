# -*- coding: utf-8 -*-

from chcko.util import PageBase
from chcko.db import db

class Page(PageBase):

    def __init__(self):
        super().__init__()
        self.request.params.update({'failed': False})

    def post_response(self):
        email = self.request.params.get('email','')
        password = self.request.forms.get('password','')
        if not (email and password):
            self.redirect('message?msg=f')
        try:
            self.request.user = db.user_by_login(email,password)
            self.renew_token()
            db.set_student(self.request,self.response)
            self.redirect('todo')
        except (ValueError, AttributeError):
            self.request.params.update({
                'email': email,
                'failed': True
            })
            return self.get_response()

