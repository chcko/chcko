# -*- coding: utf-8 -*-

from chcko.util import PageBase
import logging
from webapp2_extras.auth import InvalidAuthIdError, InvalidPasswordError


class Page(PageBase):

    def __init__(self, _request):
        super(self.__class__, self).__init__(_request)
        self.params = {'username': '', 'failed': False}

    def post_response(self):
        username = self.request.get('username')
        password = self.request.get('password')
        if not (username and password):
            self.redirect('message?msg=f')
            return
        try:
            u = self.auth.get_user_by_password(
                username,
                password,
                remember=True,
                save_session=True)
            self.redirect('todo')
        except (InvalidAuthIdError, InvalidPasswordError) as e:
            logging.warning(
                'Login failed for user %s because of %s',
                username,
                type(e))
            self.params = {
                'username': username,
                'failed': True
            }
            return self.get_response()
