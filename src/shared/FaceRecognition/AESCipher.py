import base64
import hashlib

from Crypto import Random
from Crypto.Cipher import AES


class AESCipher:
    # https://stackabuse.com/encoding-and-decoding-base64-strings-in-python/

    def __init__(self, key):
        self.key = None
        self.bs = None
        self.CreateKeyAES(key)

    def CreateKeyAES(self, key):
        self.bs = AES.block_size
        self.key = hashlib.sha256(key.encode()).digest()

    def encrypt(self, raw):
        raw = self._pad(raw)
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        data_end = base64.b64encode(iv + cipher.encrypt(raw.encode()))
        return data_end.decode("ascii")

    def decrypt(self, enc):
        enc = enc.encode("ascii")
        enc = base64.b64decode(enc)
        iv = enc[: AES.block_size]
        cipher = AES.new(self.key, AES.MODE_CBC, iv)

        data_decoded = cipher.decrypt(enc[AES.block_size:])
        return self._unpad(data_decoded).decode("utf-8")

    def _pad(self, s):
        padding = self.bs - len(s) % self.bs
        return s + (padding) * chr(padding)

    @staticmethod
    def _unpad(s):
        return s[:-ord(s[len(s) - 1:])]
