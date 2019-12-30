# -*- coding: utf-8 -*-

import os
from chcko.util import PageBase
from chcko.hlp import import_module, is_standard_server, logger
from chcko.db import db

class Page(PageBase):

    def post_response(self):
        email = self.request.get('email').strip()
        password = self.request.get('password')
        name = self.request.get('name')
        last_name = self.request.get('lastname')

        if not email or not password:
            self.redirect('message?msg=f')
            return

        if not password or password != self.request.get('confirmp'):
            self.redirect('message?msg=c')
            return

        user = db.user_create(email,password)
        if not user:
            self.redirect(
                'message?msg=a&email={}'.format(email))
            return

        token = db.token_create(email)
        relative_url = 'verification?type=v&email={}&signup_token={}'.format(
            email,
            token)

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
