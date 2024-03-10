import hashlib
import hmac

from tools.tools import to_bytes


class HASHManager:
    @staticmethod
    def calc_md5(message):
        md5 = hashlib.md5()
        md5.update(to_bytes(message))
        return md5.hexdigest()

    @staticmethod
    def calc_hmac(key, message):
        return hmac.new(to_bytes(key), to_bytes(message), 'MD5').hexdigest()
