# -*- coding: utf-8 -*-

import os
from chcko.chcko.util import PageBase
from chcko.chcko.hlp import chcko_import, logger
from chcko.chcko.auth import send_mail, newurl
from chcko.chcko.db import db

class Page(PageBase):

    def __init__(self, mod):
        super().__init__(mod)
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
        qry = f'type=p&email={self.email}&token={token}'

        try:
            chckotesting = os.environ['CHCKOTESTING'].lower()!='no'
        except:
            chckotesting = False

        confirmation_url = newurl('/{self.request.lang}/verification',qry,'')
        logger.info(confirmation_url)
        m = chcko_import('chcko.forgot.' + self.request.lang)
        if send_mail(
                self.email,
                m.subject,
                m.body %
                confirmation_url):
            self.redirect('message?msg=j')
        elif not chckotesting:
            # else we need to inform that email does not work on this server
            self.redirect('message?msg=m')
        else:
            self.redirect(f'verification?{qry}&verified=0')

