import os

import requests

from api.models.user_model import CustomUser

AUTH0_DOMAIN = os.getenv("AUTH0_DOMAIN")
AUTH0_CLIENT_ID = os.getenv("AUTH0_CLIENT_ID")
AUTH0_CLIENT_SECRET = os.getenv("AUTH0_CLIENT_SECRET")
AUTH0_AUDIENCE = os.getenv("AUTH0_AUDIENCE", f"https://{AUTH0_DOMAIN}/api/v2/")


def get_auth0_token():
    url = f"https://{AUTH0_DOMAIN}/oauth/token"
    payload = {
        "client_id": AUTH0_CLIENT_ID,
        "client_secret": AUTH0_CLIENT_SECRET,
        "audience": AUTH0_AUDIENCE,
        "grant_type": "client_credentials",
    }
    headers = {"Content-Type": "application/json"}
    response = requests.post(url, json=payload, headers=headers)
    return response.json()["access_token"]


def create_auth0_user(username, nickname, email, password, role):
    token = get_auth0_token()
    url = f"https://{AUTH0_DOMAIN}/api/v2/users"
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    data = {
        "username": username,
        "nickname": nickname,
        "email": email,
        "password": password,
        "connection": "Username-Password-Authentication",
        "user_metadata": {"role": role},
    }
    try:
        response = requests.post(url, json=data, headers=headers)
        return response.json()
    except requests.RequestException as e:
        return {"error": str(e)}


def update_auth0_user(auth0_id, **kwargs):
    """
    Update an Auth0 user with flexible fields.

    Args:
        auth0_id: The Auth0 user ID
        **kwargs: Any fields to update (username, nickname, email, password, role, etc.)

    Returns:
        dict: Auth0 API response
    """
    token = get_auth0_token()
    url = f"https://{AUTH0_DOMAIN}/api/v2/users/{auth0_id}"
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

    data = {}
    if "username" in kwargs:
        data["username"] = kwargs["username"]
    if "nickname" in kwargs:
        data["nickname"] = kwargs["nickname"]
    if "email" in kwargs:
        data["email"] = kwargs["email"]
    if "password" in kwargs:
        data["password"] = kwargs["password"]
    if "role" in kwargs:
        data["user_metadata"] = {"role": kwargs["role"]}

    try:
        # cannot update username, password and email simultaneously in Auth0
        if "username" in data:
            response = requests.patch(
                url, json={"username": data["username"]}, headers=headers
            )
            data.pop("username")
        if len(data.values()) > 0:
            response = requests.patch(url, json=data, headers=headers)
            if response.status_code != 200:
                raise Exception(
                    f"Auth0 update failed: {response.json().get('message')}"
                )
            return response.json()
    except requests.RequestException as e:
        return {"error": str(e)}


def delete_auth0_user(auth0_id):
    token = get_auth0_token()
    url = f"https://{AUTH0_DOMAIN}/api/v2/users/{auth0_id}"
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.delete(url, headers=headers)
    return response.status_code == 204
