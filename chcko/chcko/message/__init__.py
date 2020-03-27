from chcko.chcko.util import PageBase
from chcko.chcko.bottle import template
from chcko.chcko.hlp import mklookup

class Page(PageBase):
    def get_response(self,**kwextra):
        try:
            lang = self.request.lang
        except:
            lang = 'en'
        res = template('chcko.message',**kwextra,template_lookup=mklookup(lang))
        return res
