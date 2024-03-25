import hmac
import hashlib

key = "e179017a-62b0-4996-8a38-e91aa9f1"
msg = "Test"

def sign(pre_key, imsg, alg):
    return hmac.new(pre_key, imsg, alg).digest()

def verify(msg, sig):
    return sig == sign(key, msg, hashlib.sha256) #bad
