# -*- coding: utf-8 -*-

import os
import logging
from chcko.util import PageBase
from chcko.hlp import import_module, email_enabled, py_test
from google.appengine.api import mail

class Page(PageBase):

    def __init__(self, _request):
        super(self.__class__, self).__init__(_request)
        username = self.request.get('username')
        self.params = {'username': username, 'not_found': False}

    def post_response(self):
        username = self.request.get('username')

        user = self.user_model.get_by_auth_id(username)
        if not user:
            self.params = {
                'username': username,
                'not_found': True
            }
            return self.get_response()

        user_id = user.get_id()
        token = self.user_model.create_signup_token(user_id)

        relative_url = 'verification?type=p&user_id={}&signup_token={}'.format(
            user_id,
            token)

        email = ''
        try:
            email = user.email_address
        except:
            logging.warning('!! no email for password change !!')

        if not py_test and email_enabled and email:
            confirmation_url = self.request.application_url + \
                '/' + self.request.lang + '/' + relative_url
            logging.info(confirmation_url)
            m = import_module('forgot.' + self.request.lang)
            mail.send_mail(
                m.sender_address,
                email,
                m.subject,
                m.body %
                confirmation_url)
            self.redirect('message?msg=j')
        else:
            self.redirect(relative_url)
