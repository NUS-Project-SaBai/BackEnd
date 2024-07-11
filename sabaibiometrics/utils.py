import json
import jwt
from api.models import JWKS
from django.contrib.auth import authenticate
from sabaibiometrics.settings import AUTH0_ISSUER, AUTH0_AUDIENCE


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

    return jwt.decode(token, public_key, audience=AUTH0_AUDIENCE, issuer=AUTH0_ISSUER, algorithms=['RS256'])


def get_doctor_id(request):
    if "Authorization" in request.headers:
        token = request.headers["Authorization"].split(" ")[1]
        payload = jwt_decode_token(token)
        doctor_id = payload.get("sub")
        return doctor_id
