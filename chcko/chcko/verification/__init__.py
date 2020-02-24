# -*- coding: utf-8 -*-

from chcko.chcko.util import PageBase
from chcko.chcko.db import db

class Page(PageBase):

    def get_response(self):
        token = self.request.params.get('token')
        user = self.request.user
        if not user:
            self.redirect(f'message?msg=k&token={token}')
        verification_type = self.request.params.get('type')
        if verification_type == 'v':
            self.renew_token()
            if not user.verified:
                user.verified = self.request.params.get('verified','1')!='0'
                db.save(user)
            self.redirect('message?msg=b')
        elif verification_type == 'p':
            self.redirect(f'password?token={token}')
        else:
            self.redirect('message?msg=l')
