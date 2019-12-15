# -*- coding: utf-8 -*-

from chcko.util import PageBase
import webapp2
import logging


class Page(PageBase):

    def get_response(self):
        user_id = self.request.get('user_id')
        signup_token = self.request.get('signup_token')
        verification_type = self.request.get('type')

        user = None
        try:
            user, ts = self.user_model.get_by_auth_token(
                int(user_id), signup_token, 'signup')
        except:
            pass

        if not user:
            self.redirect(
                'message?msg=k&user_id=%s&signup_token=%s' %
                (user_id, signup_token))
            return

        self.auth.set_session(
            self.auth.store.user_to_dict(user),
            remember=True)

        if verification_type == 'v':
            # remove signup token to prevent users to come back with an old link
            self.user_model.delete_signup_token(user.get_id(), signup_token)
            if not user.verified:
                user.verified = True
                user.put()
            self.redirect('message?msg=b')
        elif verification_type == 'p':
            self.redirect('password?token={}'.format(signup_token))
        else:
            self.redirect('message?msg=l')
