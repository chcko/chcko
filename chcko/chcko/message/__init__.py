from chcko.chcko.util import PageBase
from chcko.chcko.bottle import template
from chcko.chcko.hlp import mklookup

class Page(PageBase):
    def get_response(self,**kwextra):
        try:
            chlang = self.request.chlang
        except:
            chlang = 'en'
        res = template('chcko.message',**kwextra,template_lookup=mklookup(chlang))
        return res
