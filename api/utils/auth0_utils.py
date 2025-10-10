import os

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


def create_auth0_user(email, password, role):
    token = get_auth0_token()
    url = f"https://{AUTH0_DOMAIN}/api/v2/users"
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    data = {
        "email": email,
        "password": password,
        "connection": "Username-Password-Authentication",
        "user_metadata": {"role": role},
    }
    response = requests.post(url, json=data, headers=headers)
    return response.json()


def update_auth0_user(auth0_id, role=None):
    token = get_auth0_token()
    url = f"https://{AUTH0_DOMAIN}/api/v2/users/{auth0_id}"
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    data = {}
    if role:
        data["user_metadata"] = {"role": role}

    response = requests.patch(url, json=data, headers=headers)
    return response.json()


def delete_auth0_user(auth0_id):
    token = get_auth0_token()
    url = f"https://{AUTH0_DOMAIN}/api/v2/users/{auth0_id}"
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.delete(url, headers=headers)
    return response.status_code == 204
