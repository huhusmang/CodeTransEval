import hashlib


def certificate_matches_known_hash(certificate, known_hash):
    hash = hashlib.sha256(certificate).hexdigest()
    return hash == known_hash