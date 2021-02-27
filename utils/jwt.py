import jwt
from datetime import datetime, timedelta
ALGORITHM = 'HS256'
JWT_SECRET = 'technical-test-backend'


class JwtHelper:
    def encode(self, payload):
        payload['iat'] = datetime.utcnow()
        payload['exp'] = datetime.utcnow() + timedelta(hours=2)
        payload['iss'] = 'ANDRES TAPIA'
        encoded = jwt.encode(payload, JWT_SECRET, algorithm=ALGORITHM)
        return encoded.decode("utf-8")

    def decode(self, encoded):
        decoded = jwt.decode(encoded, JWT_SECRET, algorithms=[ALGORITHM])
        return decoded
