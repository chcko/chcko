# -*- coding: utf-8 -*-

from chcko.util import PageBase
from chcko.db import db
import logging

class Page(PageBase):

    def get_response(self):
        signup_token = self.request.get('signup_token')
        verification_type = self.request.get('type')

        user = None
        try:
            user, _ = db.user_timestamp_by_token(signup_token, 'signup')
        except:
            pass

        if not user:
            self.redirect('message?msg=k&signup_token=%s'%signup_token)
            return

        self.auth.set_session(
            self.auth.store.user_to_dict(user),
            remember=True)

        if verification_type == 'v':
            # remove signup token to prevent users to come back with an old link
            db.delete_signup_token(signup_token)
            if not user.verified:
                user.verified = True
                user.put()
            self.redirect('message?msg=b')
        elif verification_type == 'p':
            self.redirect('password?token={}'.format(signup_token))
        else:
            self.redirect('message?msg=l')
