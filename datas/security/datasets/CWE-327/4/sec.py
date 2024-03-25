from argon2 import PasswordHasher


def check_password(password: str, known_hash):
    ph = PasswordHasher()
    return ph.verify(known_hash, password)