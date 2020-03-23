import os
import datetime
import uuid
import hashlib
from functools import lru_cache
from hmac import compare_digest
from random import choice
from urllib.parse import urlunsplit
from chcko.chcko import bottle

def newurl(path=None,query=None,fragment=None):
    p = bottle.request.urlparts
    return urlunsplit(p[:2]+(
        path is None and p[2] or path
        ,query is None and p[3] or query
        ,fragment is None and p[4] or fragment
    ))

METHOD = "pbkdf2:sha256:150000"
SALT_CHARS = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
def gen_salt():
    """
    >>> gen_salt()
    """
    return "".join(choice(SALT_CHARS) for _ in range(22))

def generate_password_hash(password):
    """
    >>> generate_password_hash('xy')
    pbkdf2:sha256:150000$hTYkIQcs$f5fe71456afb70fff81dca8647fa57a443e89f5b83a28ecfaeeb3144aa489dc1
    >>> generate_password_hash('')
    pbkdf2:sha256:150000$yBGW5hfQfpTqsJr9oAgl1y$da42d941c29933087fc9aa866ee8162d90528f63654c310b6c133c1105dec259
    """
    salt = gen_salt()
    h = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt.encode("utf-8"), 150000).hex()
    return "%s$%s$%s" % (METHOD, salt, h)

def check_password_hash(pwhash, password):
    """
    >>> pwhash = "pbkdf2:sha256:150000$hTYkIQcs$f5fe71456afb70fff81dca8647fa57a443e89f5b83a28ecfaeeb3144aa489dc1"
    >>> password = 'xy'
    >>> check_password_hash(pwhash, 'xy')
    """
    if pwhash.count("$") < 2:
        return False
    method, salt, hashval = pwhash.split("$", 2)
    if method != METHOD:
        return False
    h = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt.encode("utf-8") , 150000).hex()
    equal = compare_digest(h,hashval)
    return equal

@lru_cache()
def chckosecret():
    try:
        secret = os.environ['CHCKOSECRET']
    except:
        secret = 'CHCKOSECRET'
    return secret

def random_student_path(seed=None):
    ''' UUID parts are used as names
    >>> #myschool,myperiod,myteacher,myclass,myself = random_student_path()
    '''
    if not seed:
        seed = datetime.datetime.now().isoformat()
    while len(seed) < 16:
        seed = seed + datetime.datetime.now().isoformat().split(':')[-1]
    student_path = str(
        uuid.uuid5(
            uuid.UUID(
                bytes=seed[
                    :16].encode()),
            datetime.datetime.now().isoformat()))
    return student_path.split('-')

is_standard_server = False
if os.getenv('GAE_ENV', '').startswith('standard'):
    is_standard_server = True

#social
try:
  from social_core.strategy import BaseStrategy
  from social_core.storage import UserMixin, BaseStorage
  from functools import wraps
  # secrets are not in the repo,
  # but included via `make deploy` from local ~/my/mam/chcko/environment.yaml
  social_core_setting = {
          'SOCIAL_AUTH_SANITIZE_REDIRECTS': False
          # sign in with linkedin is not automatic but needs reviewing: therefore not tested
          # ,'SOCIAL_AUTH_LINKEDIN_OAUTH2_FIELD_SELECTORS': ['emailAddress']
          # ,'SOCIAL_AUTH_LINKEDIN_OAUTH2_EXTRA_DATA':[('id', 'id'),
          #                                    ('firstName', 'first_name'),
          #                                    ('lastName', 'last_name'),
          #                                    ('emailAddress', 'email_address')]
          # including email produces a popup, without not
          # ,'SOCIAL_AUTH_FACEBOOK_SCOPE': ['email']
          # ,'SOCIAL_AUTH_FACEBOOK_PROFILE_EXTRA_PARAMS': {
          #                                     'fields': 'id, name, email'
          #                                   }
          ,'SOCIAL_AUTH_FIELDS_STORED_IN_SESSION': []
          ,'SOCIAL_AUTH_PIPELINE': ('social_core.pipeline.social_auth.social_details'
                        ,'social_core.pipeline.social_auth.social_uid'
                        ,'social_core.pipeline.social_auth.auth_allowed'
                        ,'chcko.chcko.app.social_user'
                        )
  }
  from social_core.utils import setting_name
  from social_core.backends.google import GoogleOAuth2 as google
  from social_core.backends.facebook import FacebookOAuth2 as facebook
  from social_core.backends.linkedin import LinkedinOAuth2 as linkedin
  from social_core.backends.instagram import InstagramOAuth2 as instagram
  from social_core.backends.twitter import TwitterOAuth as twitter
  from social_core.backends.pinterest import PinterestOAuth2 as pinterest
  social_logins = {}
  for social in 'google facebook linkedin instagram twitter pinterest'.split():
      try:
          sli=globals()[social]
          for suffix in ['KEY','SECRET']:
              #'SOCIAL_AUTH_'+sli.name.upper().replace('-','_')+'_'+suffix
              envkey = setting_name(sli.name,suffix)
              social_core_setting[envkey] = os.environ[envkey]
          social_logins[social] = sli
      except:
          pass
  def social_login_name(cls):
      for k,v in social_logins.items():
          if v == cls:
              return k
  class UserModel(UserMixin):
      @classmethod
      def user_model(cls):
          return tuple # type =! dict
  class storage_for_social_core(BaseStorage):
      user = UserModel
      #pass
  class strategy_for_social_core(BaseStrategy):
      def __init__(self, storage=None, tpl=None):
          super().__init__(storage,tpl)
          self.save = {}
      def get_setting(self, name):
          return social_core_setting[name]
      def request_data(self, merge=True):
          request = bottle.request
          if merge:
              data = request.params
          elif request.method == 'POST':
              data = request.forms
          else:
              data = request.query
          return data
      def redirect(self, url):
          return bottle.redirect(url)
      def session_get(self, name, default=None):
          nn = 'chcko_'+name
          # don't return deleted cookies
          if nn in self.save and self.save[nn]=='':
              sessval = None
          else:
              sessval = bottle.request.get_cookie(nn,secret=chckosecret())
              # save needed due to session_setdefault() in social_core/strategy.py
              if sessval is None and nn in self.save:
                  sessval = self.save[nn]
          return sessval
      def session_set(self, name, value):
          nn = 'chcko_'+name
          self.save[nn] = value
          bottle.response.set_cookie(nn,value,secret=chckosecret(),maxage=datetime.timedelta(days=30))
      def session_pop(self, name):
          nn = 'chcko_'+name
          try:
              self.save[nn]=''
          except KeyError:
              pass
          bottle.response.delete_cookie(nn)
      def build_absolute_uri(self, path=None):
          return newurl(path,'','')
  def make_backend_obj():
      def decorator(func):
          @wraps(func)
          def wrapper(provider, *args, **kwargs):
              try:
                  Backend = social_logins[provider]
                  strategy = strategy_for_social_core(storage_for_social_core)
                  uri = f'/auth/{provider}/callback'
                  backend = Backend(strategy, redirect_uri=uri)
                  return func(backend, *args, **kwargs)
              except KeyError:
                  bottle.redirect('/')
          return wrapper
      return decorator
except:
  pass

# GAE had email. The hack below was a try,
# but currently no need to invest more time to make it work
with_email_verification = False
if with_email_verification:
    from googleapiclient.discovery import build
    import codecs
    import base64
    import pickle
    from google.auth.transport.requests import Request
    from google_auth_oauthlib.flow import InstalledAppFlow
    from email.mime.text import MIMEText
    pth = lambda x: os.path.join(os.path.dirname(__file__),x)
    chcko_mail = 'chcko.mail@gmail.com'
    def get_credential(
            scopes=['https://www.googleapis.com/auth/gmail.send']
            ,secret_file = pth('secret.json')
            ,token_file = pth('token.pickle')
        ):
        '''
        Tested with secret.json of chcko.mail@gmail.com for the quickstart app from
            https://developers.google.com/gmail/api/quickstart/python
        chcko.mail@gmail.com authorized manually,
        knowing that actually they are for the chcko app.
        The resulting token allows the chcko app to send emails.

        >>> pickled = codecs.encode(pickle.dumps(atoken), "base64").decode()
        >>> #pickled=CHCKO_MAIL_CREDENTIAL
        >>> unpickled = pickle.loads(codecs.decode(pickled.encode(), "base64"))
        >>> atoken == unpickled

        '''
        atoken = None
        if os.path.exists(token_file):
            with open(token_file, 'rb') as tokenf:
                atoken = pickle.load(tokenf)
        if not atoken or not atoken.valid:
            if atoken and atoken.expired and atoken.refresh_token:
                atoken.refresh(Request())
            elif os.path.exists(secret_file):
                flow = InstalledAppFlow.from_client_secrets_file(secret_file,scopes)
                atoken = flow.run_local_server(port=0)
                with open(token_file, 'wb') as tokenf:
                    pickle.dump(atoken, tokenf)
        return atoken

    @lru_cache()
    def email_credential():
        try:
            # ~/my/mam/chcko/environment.yaml
            pickled = os.environ['CHCKO_MAIL_CREDENTIAL']
            creds = pickle.loads(codecs.decode(pickled.encode(), "base64"))
        except:
            creds = get_credential()
        return creds

    def send_mail(to, subject, message_text, sender=chcko_mail):
        '''
        >>> ( to, subject, message_text) = ('roland.puntaier@gmail.com','test 2','test second message text')
        >>> send_mail(to, subject, message_text, get_credential())
        '''
        service = build('gmail', 'v1', credentials=email_credential)
        message = MIMEText(message_text)
        message['to'] = to
        message['from'] = sender
        message['subject'] = subject
        mbody = {'raw':base64.urlsafe_b64encode(message.as_bytes()).decode()}
        message = (service.users().messages().send(userId=sender, body=mbody).execute())
        return message
else:
    def send_mail(to, subject, message_text, sender=None):
        pass

