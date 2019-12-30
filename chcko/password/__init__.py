# -*- coding: utf-8 -*-

from chcko.util import PageBase, user_required
from chcko.db import db

class Page(PageBase):

    @user_required
    def post_response(self):
        password = self.request.forms.get('password')
        old_token = self.request.get('t')

        if not password or password != self.request.forms.get('confirmp'):
            self.redirect('message?msg=c')
            return

        user = self.user
        user_set_password(user,password)
        user.put()

        db.token_delete(old_token)

        self.redirect('message?msg=d')
