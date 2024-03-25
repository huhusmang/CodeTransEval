from Crypto.Cipher import DES, AES

SECRET_KEY = '12345678'
cipher = AES.new(SECRET_KEY)

def send_encrypted(channel, message):
    channel.send(cipher.encrypt(message))
