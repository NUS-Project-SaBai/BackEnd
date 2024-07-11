import json
import os
import jwt
from dotenv import load_dotenv
from api.models import JWKS

from django.contrib.auth import authenticate

# Load environment variables from the .env file
load_dotenv()


def jwt_get_username_from_payload_handler(payload):
    auth0_id = payload.get('sub')
    authenticate(remote_user=auth0_id)
    return auth0_id


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


def get_doctor_id(request):
    if "Authorization" in request.headers:
        token = request.headers["Authorization"].split(" ")[1]
        payload = jwt_decode_token(token)
        doctor_id = payload.get("sub")
        return doctor_id
