# -*- coding: utf-8 -*-

import os
from chcko.chcko.util import PageBase
from chcko.chcko.hlp import chcko_import, logger
from chcko.chcko.auth import send_mail
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
            user,token = db.user_login(email,fullname=f"{fullname}"
                                       ,password=password,lang=self.request.lang,verified=False)
        except ValueError:
            # if user exists and has different password
            self.redirect(f'message?msg=a&email={email}')

        relative_url = f'verification?type=v&email={email}&token={token}'

        domain = self.request.url
        confirmation_url = f'{domain}/{self.request.lang}/{relative_url}'
        logger.info(confirmation_url)
        m = chcko_import('chcko.signup.' + self.request.lang)
        if send_mail(
                email,
                m.subject,
                m.body %
                confirmation_url):
            self.redirect('message?msg=j')
        # else just do without email verification
        relative_url = relative_url+'&verified=0'
        self.redirect(relative_url)
