import base64
import json
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

class Decrypt:

    def __init__(self, enc_data, key):

        self.enc_data = enc_data
        self.key = key

    def decrypt_aes(self):

        key = base64.b64decode(self.key)

        decoded = base64.b64decode(self.enc_data)
        data = json.loads(decoded)
        iv = base64.b64decode(data["iv"])
        ciphertext = base64.b64decode(data["value"])

        cipher = AES.new(key, AES.MODE_CBC, iv)
        decrypted = unpad(cipher.decrypt(ciphertext), AES.block_size)

        return decrypted.decode() 