# -*- coding: utf-8 -*-

from chcko.util import PageBase, user_required

class Page(PageBase):

    @user_required
    def post_response(self):
        password = self.request.get('password')
        old_token = self.request.get('t')

        if not password or password != self.request.get('confirmp'):
            self.redirect('message?msg=c')
            return

        user = self.user
        user.set_password(password)
        user.put()

        # remove signup token, we don't want users to come back with an old
        # link
        self.user_model.delete_signup_token(user.get_id(), old_token)

        self.redirect('message?msg=d')
