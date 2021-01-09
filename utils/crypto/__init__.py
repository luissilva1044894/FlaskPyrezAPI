#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
#secret_key must be 32 url-safe` base64-encoded bytes
secret_key = base64.urlsafe_b64decode(Fernet.generate_key())

#https://github.com/coleifer/peewee/
#https://www.reddit.com/r/learnpython/comments/cro91g/reading_fernet_key_from_file/
'''

import base64
from cryptography.fernet import Fernet, InvalidToken
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers import (
  algorithms,
  Cipher,
  modes,
)
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import hashlib
import os

#https://github.com/closeio/flask-common/blob/master/flask_common/crypto.py
#https://cryptography.io/en/latest/fernet.html#using-passwords-with-fernet

#cryptography.fernet.InvalidToken
#AttributeError, TypeError, ValueError

def decrypt(token:bytes, key:bytes=None) -> bytes:
  """Decrypts Fernet encrypted strings"""
  #return Fernet(key or load_key()).decrypt(token)
  return Fernet(fix_key(key)).decrypt(token)

def encrypt(msg:bytes, key:bytes=None) -> bytes:
  """Encrypts strings using Fernet"""
  #return Fernet(key or load_key()).encrypt(msg.encode())
  #if isinstance(key, str) is False:
  #  key = generate_key(key)
  return Fernet(fix_key(key)).encrypt(to_bytes(msg))

def fix_key(key):
  if key and not str(key).endswith('='):
    return f"{key}=".encode()
  return key

def generate_key(password=None, *, length=32):
  """Generates a key and save it into a file"""
  if password:
    kdf = PBKDF2HMAC(algorithm=hashes.SHA256(), length=length, salt=os.urandom(length//2), iterations=100000, backend=default_backend())
    return base64.urlsafe_b64encode(kdf.derive(to_bytes(password)))
  #with open('secret.key', 'wb') as f: f.write(key)
  return Fernet.generate_key()

def hashing(msg, key):
  return hashlib.md5(f'{str(msg).lower()}{key}'.encode()).hexdigest()

  #from passlib.hash import sha256_crypt
  #print(sha256_crypt.verify("password", sha256_crypt.encrypt("password")))

def load_key():
  """Loads the key named `secret.key` from the current directory."""
  return open('secret.key', 'rb').read()

def write_key(key):
  with open('secret.key', 'wb') as f:
    f.write(key)

def to_bytes(obj):
  if not isinstance(obj, bytes):
    return str(obj).encode()
  return obj

'''
from cryptography.fernet import Fernet, InvalidToken
encrypted = b"...encrypted bytes..."

f = Fernet(incorrect_key)  # An example of providing the incorrect key
try:
  decrypted = f.decrypt(encrypted)
  print("Valid Key - Successfully decrypted")
except InvalidToken as e:  # Catch any InvalidToken exceptions if the correct key was not provided
  print("Invalid Key - Unsuccessfully decrypted")

>>> from cryptography.fernet import Fernet
>>> message = "my deep dark secret".encode()  # .encode() is used to turn the string to bytes
>>> f = Fernet(Fernet.generate_key())# Store this key or get if you already have it
>>> encrypted = f.encrypt(message)
>>> decrypted = f.decrypt(encrypted)
>>> message == decrypted  # The original message and decrypted bytes are the same
True

https://developer.ibm.com/technologies/blockchain/tutorials/develop-a-blockchain-application-from-scratch-in-python/
https://docs.pycom.io/firmwareapi/pycom/aes/
https://nitratine.net/blog/post/encryption-and-decryption-in-python/
https://docs.python-guide.org/writing/logging/#logging-in-a-library

key = generate_key()
cipher_text = encrypt(b'A really secret message. Not for prying eyes.', key)
plain_text = decrypt(cipher_text, key)

def main():
  """
  If you are encrypting or decrypting, you need to pass the message as bytes,
  so use .encode() on the string. If you want to write to a plaintext file,
  use .decode() and then .encode() on the read in string(s).
  """

  key = Fernet.generate_key()
  keyDecode = key.decode()
  plainText = "The answer: 42"
  et = encrypt(plainText.encode(), key)
  etDecode = et.decode()
  dt = decrypt(et, key)
  dtDecode = decrypt(et, key).decode()

  print(f"Key.encode():\t{key}")
  print(f"Key.decode():\t{keyDecode}")
  print(f"\nPlainText:\t{plainText}")
  print(f"et.encode():\t{et}")
  print(f"et.decode():\t{etDecode}")
  print(f"dt.encode():\t{dt}")
  print(f"dt.decode():\t{dtDecode}")

  with open('fernet.key', 'w') as f:
    f.write(keyDecode)
  with open('eMessage.txt', 'w') as f:
    f.write(etDecode)
  with open('fernet.key', 'r') as f:
    fileKey = f.readline()
  with open('eMessage.txt', 'r') as f:
    eMessage = f.readline()
  print(f"\nFile.decode():\t{decrypt(eMessage.encode(), fileKey).decode()}")

if __name__ == '__main__':
  main()
import hmac
import hashlib

def create_signature(msg, secret_key, digest_mod=None):
  mac = hmac.new(secret_key, msg=msg, digestmod=digest_mod or hashlib.sha1)
  return mac.digest()
create_signature('aaaaaaa'.encode('utf8'), 'bbbbb'.encode('utf8'))

import uuid
uuid.uuid4().hex

import os
os.urandom(12)

#https://docs.python.org/3/library/secrets.html
import secrets
secrets.token_urlsafe(16)
secrets.token_hex(16)

import os
os.urandom(12).hex()


from itsdangerous.url_safe import URLSafeSerializer
s = URLSafeSerializer("secret-key")
s.dumps([1, 2, 3, 4])
'WzEsMiwzLDRd.wSPHqC0gR7VUqivlSukJ0IeTDgo'
s.loads("WzEsMiwzLDRd.wSPHqC0gR7VUqivlSukJ0IeTDgo")
[1, 2, 3, 4]



from itsdangerous import Signer
s = Signer("secret-key")
s.sign("my string")
b'my string.wh6tMHxLgJqB6oY1uT73iMlyrOA'
s.unsign(b"my string.wh6tMHxLgJqB6oY1uT73iMlyrOA")

#itsdangerous.exc.BadSignature: s.unsign(b"different string.wh6tMHxLgJqB6oY1uT73iMlyrOA")




from itsdangerous.serializer import Serializer
from itsdangerous.exc import BadSignature, BadData

s = URLSafeSerializer("secret-key")
decoded_payload = None

try:
  decoded_payload = s.loads(data)
  # This payload is decoded and safe
except BadSignature as e:
  if e.payload is not None:
    try:
      decoded_payload = s.load_payload(e.payload)
    except BadData:
      pass
    # This payload is decoded but unsafe because someone
    # tampered with the signature. The decode (load_payload)
    # step is explicit because it might be unsafe to unserialize
    # the payload (think pickle instead of json!)
sig_okay, payload = s.loads_unsafe(data)

https://itsdangerous.palletsprojects.com/en/1.1.x/timed/
https://itsdangerous.palletsprojects.com/en/1.1.x/jws/

https://stackoverflow.com/questions/30826287/use-decorators-check-user-login-in-flask
https://github.com/singingwolfboy/flask-dance/issues/243
https://pythonhosted.org/Flask-Principal/
https://github.com/singingwolfboy/flask-dance-multi-provider
https://github.com/lingthio/Flask-User/blob/master/flask_user/decorators.py
https://blog.tecladocode.com/protecting-endpoints-in-flask-apps-by-requiring-login/
https://stackoverflow.com/questions/46661083/how-to-set-cookie-in-python-flask
https://overiq.com/flask-101/cookies-in-flask/
https://flask.palletsprojects.com/en/master/security/
https://itsdangerous.palletsprojects.com/en/1.1.x/encoding/
https://itsdangerous.palletsprojects.com/en/1.1.x/signer/#signing-algorithms
https://github.com/udacity/ud330/tree/master/Lesson2/step7
https://github.com/udacity/ud330/blob/master/Lesson4/step2/project.py
https://blog.miguelgrinberg.com/post/how-secure-is-the-flask-user-session


import hashlib
password = 'pa$$w0rd'
h = hashlib.md5(password.encode())
print(h.hexdigest())


import hashlib

user_entered_password = 'pa$$w0rd'
salt = "5gz"
db_password = user_entered_password+salt
h = hashlib.md5(db_password.encode())
print(h.hexdigest())
'''