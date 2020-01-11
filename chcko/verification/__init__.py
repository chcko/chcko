# -*- coding: utf-8 -*-

from chcko.util import PageBase
from chcko.db import db

class Page(PageBase):

    def get_response(self):
        token = self.request.params.get('token')
        verification_type = self.request.params.get('type')

        user = None
        try:
            user = db.user_by_token(token)
        except:
            pass

        if not user:
            self.redirect(f'message?msg=k&token={token}')
            return

        if verification_type == 'v':
            # remove signup token to prevent users to come back with an old link
            self.request.user = user
            self.renew_token(token)
            if not user.verified:
                user.verified = True
                db.save(user)
            self.redirect('message?msg=b')
        elif verification_type == 'p':
            self.redirect(f'password?token={token}')
        else:
            self.redirect('message?msg=l')
