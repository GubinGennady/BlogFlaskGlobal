import hashlib


def hash_password(password):
    a = hashlib.sha256()
    a.update(password.encode())
    return a.hexdigest()