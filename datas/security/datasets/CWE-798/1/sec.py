import hashlib
import binascii
from django.shortcuts import redirect

CONFIG_FILE = "config.ini"

def process_request(request):
    password = request.GET["password"]

    hashed_password = load_from_config('hashed_password', CONFIG_FILE)
    salt = load_from_config('salt', CONFIG_FILE)

    dk = hashlib.pbkdf2_hmac('sha256', password, salt, 100000)
    hashed_input = binascii.hexlify(dk)
    if hashed_input == hashed_password:
        redirect("login")


def load_from_config(key, config_file):
    with open(config_file, 'r') as f:
        config = f.read()
    return config.split(key + '=')[1].split('\n')[0]