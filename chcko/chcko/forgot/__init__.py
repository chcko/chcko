# -*- coding: utf-8 -*-

import os
from chcko.chcko.util import PageBase
from chcko.chcko.hlp import chcko_import, is_standard_server, logger
from chcko.chcko.db import db

class Page(PageBase):

    def __init__(self):
        super().__init__()
        self.not_found = False
        self.email = self.request.params.get('email','')
        if self.email:
            self.user = db.Key(db.User,self.email).get()
            self.not_found = self.user == None
        else:
            self.user = None
        self.request.params.update({
            'email': self.email,
            'not_found': self.not_found
        })

    def post_response(self):
        if self.not_found:
            self.redirect(f'signup?email={self.email}')

        token = db.token_create(self.email) #not in user.token = signup token
        relative_url = f'verification?type=p&email={self.email}&token={token}'

        if is_standard_server:
            domain = self.request.application_url
            confirmation_url = f'{domain}/{self.request.lang}/{relative_url}'
            logger.info(confirmation_url)
            m = chcko_import('chcko.forgot.' + self.request.lang)
            db.send_mail(
                self.email,
                m.subject,
                m.body %
                confirmation_url)
            self.redirect('message?msg=j')
        else:
            self.redirect(relative_url)
