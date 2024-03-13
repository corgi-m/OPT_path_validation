import hashlib
import hmac
import random
from abc import ABC
from functools import wraps

from Crypto.Cipher import AES
from Crypto.Cipher import PKCS1_v1_5 as RSAENC
from Crypto.Hash import SHA384
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5 as RSASIGN

from tools.tools import to_bytes


class ABCLayer(ABC):
    name = 'BaseLayer'

    def __init__(self, node):
        ...

    @staticmethod
    def to_bytes(func):
        @wraps(func)
        def fun(*args):
            args = [to_bytes(i) for i in args]
            result = func(*args)
            return to_bytes(result) if type(result) is not bool else result

        return fun

    @staticmethod
    @to_bytes
    def H(message):
        md5 = hashlib.md5()
        md5.update(message)
        return md5.hexdigest()

    @staticmethod
    @to_bytes
    def MAC(key, message):
        return hmac.new(key, message, 'MD5').hexdigest()

    @staticmethod
    @to_bytes
    def AESEncrypt(key, message):
        aes = AES.new(key[:16], AES.MODE_EAX, nonce=key[16:])
        aes.encrypt(message)
        return message

    @staticmethod
    @to_bytes
    def AESDecrypt(key, message):
        aes = AES.new(key[:16], AES.MODE_EAX, nonce=key[16:])
        aes.decrypt(message)
        return message

    @staticmethod
    @to_bytes
    def RSAEncrypt(key, message):
        key = RSA.import_key(key)
        rsa = RSAENC.new(key)
        # logging.debug(rsa.encrypt(message))
        return rsa.encrypt(message)

    @staticmethod
    @to_bytes
    def RSADecrypt(key, message):
        key = RSA.import_key(key)
        rsa = RSAENC.new(key)
        return rsa.decrypt(message, 'error').decode()

    @staticmethod
    @to_bytes
    def RSASign(key, message):
        key = RSA.import_key(key)
        rsa = RSASIGN.new(key)
        message = SHA384.new(message)
        return rsa.sign(message)

    @staticmethod
    @to_bytes
    def RSACheck(key, message, sign):
        key = RSA.import_key(key)
        rsa = RSASIGN.new(key)
        message = SHA384.new(message)
        try:
            rsa.verify(message, sign)
        except:
            return False
        return True

    @staticmethod
    @to_bytes
    def SymKeyGen(size=32):
        return random.randbytes(size)

    @staticmethod
    @to_bytes
    def ASymKeyGen():
        key = RSA.generate(1024, random.randbytes)
        SK = key.export_key()
        PK = key.publickey().export_key()
        return SK, PK

    @classmethod
    def get_name(cls):
        return cls.name