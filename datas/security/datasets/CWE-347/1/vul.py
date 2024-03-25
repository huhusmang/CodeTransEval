import jwt

jwt.decode(payload, key="somekey", verify=False)
