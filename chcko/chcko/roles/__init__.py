# -*- coding: utf-8 -*-

from chcko.chcko.util import PageBase, user_required


class Page(PageBase):

    @user_required
    def get_response(self):
        return super(Page, self).get_response()
