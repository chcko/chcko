import os
import datetime
import uuid
import hashlib
import jwt as pyjwt
from functools import lru_cache
from hmac import compare_digest
from random import choice
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

@lru_cache
def chckosecret():
    try:
        secret = os.environ['CHCKOSECRET']
    except:
        secret = 'CHCKOSECRET'
    return secret

def jwtcode(jwt):
    #jwt = {'access_token': 'D447qOKuh0v48OVTNQ7sj2Bj1uux0Kk5AA01kOFbM5',
    #   'expires_in': 864000, 'scope': ['profile', 'email'], 'token_type': 'Bearer', 'expires_at': 1582360976.518611}
    try:
        jwt = pyjwt.encode(jwt,chckosecret())
    except:
        jwt = pyjwt.decode(jwt,chckosecret())
    return jwt

def random_student_path(seed=None):
    ''' UUID parts are used as names
    >>> #myschool,myperiod,myteacher,myclass,myself = random_student_path().split('-')
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
    return student_path

is_standard_server = False
if os.getenv('GAE_ENV', '').startswith('standard'):
  is_standard_server = True

#AUTH
from chcko.chcko import bottle
from urllib.parse import urljoin
from functools import wraps
from social_core.strategy import BaseStrategy
from social_core.storage import UserMixin,BaseStorage
#from social_core.backends.google import GoogleOAuth2 as google
from social_core.backends.oauth import BaseOAuth2
class BaseLocalAuth(object):
    def get_user_id(self, details, response):
        """Use google email as unique id"""
        if self.setting('USE_UNIQUE_USER_ID', False):
            if 'sub' in response:
                return response['sub']
            else:
                return response['id']
        else:
            return details['email']
    def get_user_details(self, response):
        """Return user details from Local API account"""
        if 'email' in response:
            email = response['email']
        else:
            email = ''
        name, given_name, family_name = (
            response.get('name', ''),
            response.get('given_name', ''),
            response.get('family_name', ''),
        )
        fullname, first_name, last_name = self.get_user_names(
            name, given_name, family_name
        )
        return {'username': email.split('@', 1)[0],
                'email': email,
                'fullname': fullname,
                'first_name': first_name,
                'last_name': last_name}
class BaseLocalOAuth2API(BaseLocalAuth):
    def user_data(self, access_token, *args, **kwargs):
        """Return user data from Local API"""
        return self.get_json(
            'http://localhost:5000/api/me',
            headers={
                'Authorization': 'Bearer %s' % access_token,
            },
        )
    def revoke_token_params(self, token, uid):
        return {'token': token}
    def revoke_token_headers(self, token, uid):
        return {'Content-type': 'application/json'}
class local(BaseLocalOAuth2API, BaseOAuth2):
    """
    CLI1::
      /mnt/src/example-oauth2-server
      rm website/sqlite.db
      flask run
      #in browser:
      #enter username
      #create client 
          # Local,http://localhost:8080,profile email,http://localhost:8080/auth/local/callback
          # authorization_code, code
    CLI2::
      ~/mine/chcko
      export OAUTHLIB_INSECURE_TRANSPORT=1
      #as given on the example-oauth2-server page
      export LOCAL_CLIENT_ID="GAy9OcsNjCAlWqB9dPw7pWWK"
      export LOCAL_CLIENT_SECRET="nC0vbG3az6UZfyUs0PCcm0MqzY6OMbT7B9eOGrDgl3HIqqw3"
      ./runchcko_with_sql.py
    """
    name = 'local'
    REDIRECT_STATE = False
    AUTHORIZATION_URL = 'http://localhost:5000/oauth/authorize'
    ACCESS_TOKEN_URL = 'http://localhost:5000/oauth/token'
    ACCESS_TOKEN_METHOD = 'POST'
    REVOKE_TOKEN_URL = 'http://localhost:5000/oauth/revoke'
    REVOKE_TOKEN_METHOD = 'GET'
    DEFAULT_SCOPE = ['email', 'profile']
    EXTRA_DATA = [
        ('refresh_token', 'refresh_token', True),
        ('expires_in', 'expires'),
        ('token_type', 'token_type', True)
    ]
social_logins = {}
for social in 'local google facebook linkedin instagram twitter pinterest'.split():
    try:
        social_logins[social]=globals()[social]
    except:
        pass
social_core_setting = {
        'SOCIAL_AUTH_SANITIZE_REDIRECTS': False
        ,'SOCIAL_AUTH_LOCAL_FIELDS_STORED_IN_SESSION': []
        ,'SOCIAL_AUTH_LOCAL_KEY': "92pSnHmecuU9F66SXutV5A1h"
        ,'SOCIAL_AUTH_LOCAL_SECRET': "1FuSRKIM6VKzilZcQm0mfRss0pMtX9f93FrTsD2A17aJlcgN"
        ,'SOCIAL_AUTH_PIPELINE': ('social_core.pipeline.social_auth.social_details'
                      ,'social_core.pipeline.social_auth.social_uid'
                      ,'social_core.pipeline.social_auth.auth_allowed'
                      ,'chcko.chcko.app.social_user'
                      )
}
class UserModel(UserMixin):
#    @classmethod
#    def clean_username(cls, value):
#        return None
#    @classmethod
#    def changed(cls, user):
#        return None
#    @classmethod
#    def get_username(cls, user):
#        return None
    @classmethod
    def user_model(cls):
        return tuple # type =! dict
#    @classmethod
#    def username_max_length(cls):
#        return None
#    @classmethod
#    def allowed_to_disconnect(cls, user, backend_name, association_id=None):
#        return None
#    @classmethod
#    def disconnect(cls, entry):
#        return None
#    @classmethod
#    def user_exists(cls, *args, **kwargs):
#        return None
#    @classmethod
#    def create_user(cls, *args, **kwargs):
#        return None
#    @classmethod
#    def get_user(cls, pk):
#        return None
#    @classmethod
#    def get_users_by_email(cls, email):
#        return None
#    @classmethod
#    def get_social_auth(cls, provider, uid):
#        if not isinstance(uid, six.string_types):
#            uid = str(uid)
#        try:
#            return cls._query().filter_by(provider=provider,
#                                          uid=uid)[0]
#        except IndexError:
#            return None
#        return None
#    @classmethod
#    def get_social_auth_for_user(cls, user, provider=None, id=None):
#        return None
#    @classmethod
#    def create_social_auth(cls, user, uid, provider):
#        return None

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
        sessval = bottle.request.get_cookie(nn)
        if sessval is None and nn in self.save:
            sessval = self.save[nn]
        return sessval
    def session_set(self, name, value):
        nn = 'chcko_'+name
        self.save[nn] = value
        #bottle.response.set_cookie(nn,value,httponly=True,path='/',samesite='strict',maxage=datetime.timedelta(days=30))
        bottle.response.set_cookie(nn,value)
    def session_pop(self, name):
        nn = 'chcko_'+name
        del self.save[nn]
        bottle.response.delete_cookie(nn)
    def build_absolute_uri(self, path=None):
        return urljoin(bottle.request.url,path or '')
def make_backend_obj():
    def decorator(func):
        @wraps(func)
        def wrapper(provider, *args, **kwargs):
            uri = urljoin(bottle.request.url, f'/auth/{provider}/callback')
            strategy = strategy_for_social_core(storage_for_social_core)
            Backend = social_logins[provider]
            backend = Backend(strategy, redirect_uri=uri)
            return func(backend, *args, **kwargs)
        return wrapper
    return decorator

#email
import base64
import pickle
from googleapiclient.discovery import build
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
    '''
    atoken = None
    if os.path.exists(token_file):
        with open(token_file, 'rb') as tokenf:
            atoken = pickle.load(tokenf)
    if not atoken or not atoken.valid:
        if atoken and atoken.expired and atoken.refresh_token:
            atoken.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
              pth(secret_file),scopes)
            atoken = flow.run_local_server(port=0)
        with open(token_file, 'wb') as tokenf:
            pickle.dump(atoken, tokenf)
    return atoken

@lru_cache
def email_credential():
    try:
        creds = base64.urlsafe_b64decode(os.environ['CHCKO_MAIL_CREDENTIAL'])
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


