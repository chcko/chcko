import datetime
import uuid
import hashlib
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

def make_secret():
    '''
    >>> make_secret()
    '''
    asecret = str(uuid.uuid5(
    uuid.UUID(bytes=datetime.datetime.now().isoformat()[:16].encode()),
    datetime.datetime.now().isoformat()))
    return asecret

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
        ,credential_file = pth('credentials.json')
        ,token_file = pth('token.pickle')
    ):
    '''
    Tested with credentials.json of chcko.mail@gmail.com for the quickstart app from
        https://developers.google.com/gmail/api/quickstart/python
    chcko.mail@gmail.com authorized these credentials manually,
    knowing that actually they are for the chcko app.
    The resulting token allows the chcko app to send emails.
    '''
    creds = None
    if os.path.exists(token_file):
        with open(token_file, 'rb') as tokenf:
            creds = pickle.load(tokenf)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
              pth(credential_file),scopes)
            creds = flow.run_local_server(port=0)
        with open(token_file, 'wb') as tokenf:
            pickle.dump(creds, tokenf)
    return creds
def send_mail(to, subject, message_text, creds, sender=chcko_mail):
    '''if is_standard_server use creds=db.stored_email_credential() else get_credential()
    >>> ( to, subject, message_text) = ('roland.puntaier@gmail.com','test 2','test second message text')
    >>> send_mail(to, subject, message_text, get_credential())
    '''
    service = build('gmail', 'v1', credentials=creds)
    message = MIMEText(message_text)
    message['to'] = to
    message['from'] = sender
    message['subject'] = subject
    mbody = {'raw':base64.urlsafe_b64encode(message.as_bytes()).decode()}
    message = (service.users().messages().send(userId=sender, body=mbody).execute())
    return message
