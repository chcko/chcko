# -*- coding: utf-8 -*-

import logging
import os
from chcko.util import PageBase
from chcko.hlp import import_module, is_standard_server
from chcko.model import send_mail

class Page(PageBase):

    def post_response(self):
        user_name = self.request.get('username')
        email = self.request.get('email').strip()
        password = self.request.get('password')
        name = self.request.get('name')
        last_name = self.request.get('lastname')

        if not user_name or not email or not password:
            self.redirect('message?msg=f')
            return

        if not password or password != self.request.get('confirmp'):
            self.redirect('message?msg=c')
            return

        unique_properties = ['email_address']

        user_data = self.user_model.create_user(
            user_name,
            unique_properties,
            email_address=email,
            name=name,
            password_raw=password,
            last_name=last_name,
            verified=False)
        if not user_data[0]:  # user_data is a tuple
            self.redirect(
                'message?msg=a&username={}&email={}'.format(
                    user_name,
                    email))
            return

        user = user_data[1]
        user_id = user.get_id()

        token = self.user_model.create_signup_token(user_id)
        relative_url = 'verification?type=v&user_id={}&signup_token={}'.format(
            user_id,
            token)

        if is_standard_server:
            confirmation_url = self.request.application_url + \
                '/' + self.request.lang + '/' + relative_url
            logging.info(confirmation_url)
            m = import_module('signup.' + self.request.lang)
            send_mail(
                m.sender_address,
                email,
                m.subject,
                m.body %
                confirmation_url)
            self.redirect('message?msg=j')
        else:
            self.redirect(relative_url)
