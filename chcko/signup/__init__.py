# -*- coding: utf-8 -*-

import os
from chcko.util import PageBase
from chcko.hlp import import_module, is_standard_server, logger
from chcko.db import db

class Page(PageBase):

    def post_response(self):
        email = self.request.forms.get('email').strip()
        password = self.request.forms.get('password')
        name = self.request.forms.get('name')
        lastname = self.request.forms.get('lastname')

        if not email or not password:
            self.redirect('message?msg=f')

        if not password or password != self.request.forms.get('confirmp'):
            self.redirect('message?msg=c')

        try:
            user = db.user_create(email,password,fullname=f"{name} {lastname}")
        except ValueError:
            self.redirect(f'message?msg=a&email={email}')

        token = db.token_create(email)
        relative_url = f'verification?type=v&email={email}&token={token}'

        if is_standard_server:
            confirmation_url = self.request.application_url + \
                '/' + self.request.lang + '/' + relative_url
            logger.info(confirmation_url)
            m = import_module('signup.' + self.request.lang)
            db.send_mail(
                email,
                m.subject,
                m.body %
                confirmation_url)
            self.redirect('message?msg=j')
        else:
            self.redirect(relative_url)
