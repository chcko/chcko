# -*- coding: utf-8 -*-

from chcko.chcko.util import PageBase, user_required
from chcko.chcko.db import db

class Page(PageBase):

    @user_required
    def get_response(self):
        return super().get_response()

    @user_required
    def post_response(self):
        password = self.request.forms.get('password')

        if not password or password != self.request.forms.get('confirmp'):
            self.redirect('message?msg=c')

        self.request.user.fullname = self.request.forms.get('fullname')
        db.user_set_password(self.request.user,password)

        #this token was in addition to request.user.token
        #see forgot/__init__.py
        token = self.request.params.get('token')
        db.token_delete(token)

        self.renew_token()

        self.redirect('message?msg=d')
