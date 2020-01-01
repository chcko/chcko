# -*- coding: utf-8 -*-

import os
from chcko.util import PageBase
from chcko.hlp import import_module, is_standard_server, logger
from chcko.db import db

class Page(PageBase):

    def __init__(self, request):
        super().__init__(request)
        self.email = self.request.forms.get('Email','')
        self.params = {'email': self.email, 'not_found': False}

    def post_response(self):
        if not self.request.user:
            self.params = {
                'email': self.email,
                'not_found': True
            }
            return self.get_response()

        email = self.request.user.email
        token = db.token_create(email)

        relative_url = 'verification?type=p&email={}&signup_token={}'.format(
            email,
            token)

        email = ''
        try:
            email = user.email_address
        except:
            logger.warning('!! no email for password change !!')

        if is_standard_server and email:
            confirmation_url = self.request.application_url + \
                '/' + self.request.lang + '/' + relative_url
            logger.info(confirmation_url)
            m = import_module('forgot.' + self.request.lang)
            db.send_mail(
                email,
                m.subject,
                m.body %
                confirmation_url)
            self.redirect('message?msg=j')
        else:
            self.redirect(relative_url)
