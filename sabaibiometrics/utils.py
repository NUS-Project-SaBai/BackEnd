import json
import os
import jwt
import requests
from dotenv import load_dotenv
from api.models import JWKS

from django.contrib.auth import authenticate

# Load environment variables from the .env file
load_dotenv()


def jwt_get_username_from_payload_handler(payload):
    username = payload.get('sub')
    return username


def jwt_decode_token(token):
    header = jwt.get_unverified_header(token)
    jwks = JWKS.objects.latest('updated_at').jwks
    public_key = None
    for jwk in jwks['keys']:
        if jwk['kid'] == header['kid']:
            public_key = jwt.algorithms.RSAAlgorithm.from_jwk(json.dumps(jwk))

    if public_key is None:
        raise Exception('Public key not found.')

    issuer = f'https://{os.getenv("AUTH0_DOMAIN")}/'
    return jwt.decode(token, public_key, audience=os.getenv("AUTH0_AUDIENCE"), issuer=issuer, algorithms=['RS256'])
