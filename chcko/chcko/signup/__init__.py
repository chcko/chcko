# -*- coding: utf-8 -*-

import os
from chcko.chcko.util import PageBase
from chcko.chcko.hlp import chcko_import, logger
from chcko.chcko.auth import is_standard_server, send_mail
from chcko.chcko.db import db

class Page(PageBase):

    def post_response(self):
        email = self.request.forms.get('email').strip()
        password = self.request.forms.get('password')
        fullname = self.request.forms.get('fullname').strip()

        if not email or not password:
            self.redirect('message?msg=f')

        if not password or password != self.request.forms.get('confirmp'):
            self.redirect('message?msg=c')

        try:
            user,token = db.user_login(email,fullname=f"{fullname}",password)
        except ValueError:
            self.redirect(f'message?msg=a&email={email}')

        relative_url = f'verification?type=v&email={email}&token={token}'

        if is_standard_server:
            confirmation_url = self.request.application_url + \
                '/' + self.request.lang + '/' + relative_url
            logger.info(confirmation_url)
            m = chcko_import('chcko.signup.' + self.request.lang)
            send_mail(
                email,
                m.subject,
                m.body %
                confirmation_url)
            self.redirect('message?msg=j')
        else:
            self.redirect(relative_url)