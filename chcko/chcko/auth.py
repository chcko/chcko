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


# OAuth2
import os
import importlib
from collections import OrderedDict
from requests_oauthlib import OAuth2Session

class ProviderBase:
    Flow = OAuth2Session
    params = {}
    scope = None

    def __init__(self
                 ,client_id = None
                 ,client_secret = None
                 ):
        PROVIDER = self.id.upper()
        try:
            self.client_id = client_id or os.environ[f'{PROVIDER}_CLIENT_ID']
        except KeyError:
            self.client_id = client_id
        try:
            self.client_secret = client_secret or os.environ[f'{PROVIDER}_CLIENT_SECRET']
        except KeyError:
            self.client_secret = client_secret
        assert self.client_id
        assert self.client_secret

    def authorize(self
                 ,callback_uri
                  ):
        """Call this in your login handler

        :param callback_uri: of your app to handle provider callback

        :return url,state: Save the state as e.g. a coookie for ``authorized()`` in the callback_uri handler.
                            Redirect the browser to the returned provider URL.

        The provider will redirect to callback_uri.
        The provider adds parameters to callback_uri before redirecting.

        """
        self.flow = self.Flow(self.client_id
                          ,redirect_uri=callback_uri
                          ,scope=self.scope
                          )
        url, state = self.flow.authorization_url(self.authorize_url
                , **self.params
                )
        return url, state

    def authorized(self
                   ,callback_uri
                   ,response_uri
                   ,state
                   ,token_updater
                   ):
        """Call this in the redirect_uri handler

        :param token_updater: function that stores a refreshed access token in e.g. a cookie

        """
        self.flow = self.Flow(self.client_id
                              ,state=state
                              ,redirect_uri=callback_uri
                              )
        try:
            access_jwt = self.flow.fetch_token(self.access_token_url
                ,authorization_response=response_uri
                ,client_secret=self.client_secret
              )
            #access_jwt = {'access_token': 'D447qOKuh0v48OVTNQ7sj2Bj1uux0Kk5AA01kOFbM5',
            #   'expires_in': 864000, 'scope': ['profile', 'email'], 'token_type': 'Bearer', 'expires_at': 1582360976.518611}
            token_updater(access_jwt)
            info = self.info()
            return info
        except:
            pass

    def info(self
             ,access_jwt = None
             ,token_updater = None
             ):
        """Call this to get info.

        Provide parameters only if at a later request, i.e. not immediately after ``authorized()``.

        :param access_jwt: as returned by ``authorized``, restored e.g. form a cookie
        :param token_updater: function that stores a refreshed access token in e.g. a cookie

        """
        if access_jwt is not None:
            self.flow = self.Flow(self.client_id
                      ,token=access_jwt
                      ,auto_refresh_url=self.refresh_url
                      ,auto_refresh_kwargs=self.params
                      ,token_updater=token_updater
                      )
        try:
            profile_urls = self.profile_url if isinstance(self.profile_url,list) else [self.profile_url]
            info = {}
            for profile_url in profile_urls:
                if callable(profile_url):
                    profile_url = profile_url(**self.flow.token)
                profile = self.flow.get(profile_url)
                info.update(self.normalize(profile.json()))
            return info
        except:
            pass

    def normalize(self, data):
        return dict(data)

    @property
    def refresh_url(self):
        return self.access_token_url

class Local(ProviderBase):
    """
    CLI1::

      /mnt/src/example-oauth2-server
      rm website/sqlite.db
      flask run
      #in browser:
      #enter username
      #create client 
          # Local,http://localhost:8080,profile email,http://localhost:8080/auth/local/callback
          # authorization_code password, code

    CLI2::

      export OAUTHLIB_INSECURE_TRANSPORT=1
      #as given on the example-oauth2-server page
      export LOCAL_CLIENT_ID="dJ3tdzt5GJUCcUuGMjnUT1Pm"
      export LOCAL_CLIENT_SECRET="hiFm6LpqinbYHpWjvG4FR3FYaByqZwuRN1yMScfVvCaoFDQL"
      ~/mine/chcko
      ./runchcko_with_sql.py

    """
    id = 'local'
    name = 'Local'
    scope = 'profile email'
    def normalize(self, data):
        res = dict(data)
        res['unique_id'] = str(data['id'])
        res['name'] = data['username']
        res['email'] = data['username']+'@local.org'
        return res
    access_token_url = 'http://localhost:5000/oauth/token'
    authorize_url = 'http://localhost:5000/oauth/authorize'
    profile_url = 'http://localhost:5000/api/me'


#only those where os.environ['GOOGLE_CLIENT_ID/SECRET'] is set will get in
social_logins = {}
for social in 'local google facebook linkedin instagram twitter pinterest'.split():
    try:
        social_logins[social]=globals()[social[0].upper()+social[1:]]()
    except:
        pass

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


