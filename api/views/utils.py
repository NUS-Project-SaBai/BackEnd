from sabaibiometrics.utils import jwt_decode_token
from api.models import CustomUser


def get_doctor_id(headers):
    if "Authorization" in headers:
        token = headers["Authorization"].split(" ")[1]
        payload = jwt_decode_token(token)
        doctor_id = payload.get("sub")
        return doctor_id
    elif "doctor" in headers:
        auth0_id = CustomUser.objects.get(email=headers["doctor"]).auth0_id
        return auth0_id
