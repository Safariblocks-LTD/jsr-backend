import rsa
import json
from base64 import (
    b64encode, 
    b64decode,
)  
from utils import Responder


class Cryptography:
   
    @classmethod
    def get_public_private_keys(cls):
        public_key, private_key = rsa.newkeys(2048)
        return b64encode(public_key.save_pkcs1("PEM")).decode(), b64encode(private_key.save_pkcs1("PEM")).decode()
        
    @classmethod
    def encrypt(cls, data, public_key):
        data = json.dumps(data).replace(" ", "").encode("utf-8")
        data = rsa.encrypt(data, public_key)
        return b64encode(data).decode()
        
    @classmethod
    def decrypt(cls, data, private_key):
        try:
            private_key = rsa.PrivateKey.load_pkcs1(b64decode(private_key))
            data = rsa.decrypt(b64decode(b64decode(data)), private_key).decode()
            return json.loads(data)
        except Exception:
            Responder.raise_error(510)