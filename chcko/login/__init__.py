# -*- coding: utf-8 -*-

from chcko.util import PageBase

class Page(PageBase):

    def __init__(self, request):
        super().__init__(request)
        self.params = {'email': '', 'failed': False}

    def post_response(self):
        email = self.request.forms.get('email','')
        password = self.request.forms.get('password','')
        if not (email and password):
            self.redirect('message?msg=f')
            return
        self.request.user = db.user_by_login(email,password)
        set_student(self.request)
        self.redirect('todo')
