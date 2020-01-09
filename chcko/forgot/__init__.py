# -*- coding: utf-8 -*-

import os
from chcko.util import PageBase
from chcko.hlp import import_module, is_standard_server, logger
from chcko.db import db

class Page(PageBase):

    def __init__(self):
        super().__init__()
        self.email = self.request.forms.get('email','')
        if self.email:
            self.user = db.Key(db.User,self.email).get()
        else:
            self.user = None
        self.not_found = self.user == None
        self.request.params.update({
            'email': self.email,
            'not_found': self.not_found
        })

    def post_response(self):
        if self.not_found:
            self.redirect(f'signup?email={self.email}')

        token = db.token_create(self.email)
        relative_url = f'verification?type=p&email={self.email}&token={token}'

        if is_standard_server:
            domain = self.request.application_url
            confirmation_url = f'{domain}/{self.request.lang}/{relative_url}'
            logger.info(confirmation_url)
            m = import_module('forgot.' + self.request.lang)
            db.send_mail(
                self.email,
                m.subject,
                m.body %
                confirmation_url)
            self.redirect('message?msg=j')
        else:
            self.redirect(relative_url)
