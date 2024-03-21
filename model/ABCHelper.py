import hashlib
import hmac
import logging
import random
import time
from functools import wraps

from Crypto.Cipher import AES
from Crypto.Cipher import PKCS1_v1_5 as RSAENC
from Crypto.Hash import SHA384
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5 as RSASIGN

from tools.tools import strcat, to_bytes


class ABCHelper:
    @staticmethod
    def to_bytes(func):
        @wraps(func)
        def fun(*args):
            args = [to_bytes(i) for i in args]
            t1 = time.time()
            result = func(*args)
            t2 = time.time() - t1
            if t2 > 1:
                logging.debug(strcat(func, t2))
            return to_bytes(result) if type(result) is str else result

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
        except Exception as e:
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
