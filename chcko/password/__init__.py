# -*- coding: utf-8 -*-

from chcko.util import PageBase, user_required
from chcko.db import db

class Page(PageBase):

    @user_required
    def post_response(self):
        password = self.request.forms.get('password')
        tkn = self.request.forms.get('token')

        if not password or password != self.request.forms.get('confirmp'):
            self.redirect('message?msg=c')

        db.user_set_password(self.request.user,password)

        self.renew_token(tkn)

        self.redirect('message?msg=d')
