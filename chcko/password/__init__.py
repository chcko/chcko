# -*- coding: utf-8 -*-

from chcko.util import PageBase, user_required
from chcko.db import db

class Page(PageBase):

    @user_required
    def post_response(self):
        password = self.request.forms.get('password')
        old_token = self.request.froms.get('t')

        if not password or password != self.request.forms.get('confirmp'):
            self.redirect('message?msg=c')
            return

        user_set_password(self.request.user,password)
        self.request.user.put()

        db.token_delete(old_token)

        self.redirect('message?msg=d')
