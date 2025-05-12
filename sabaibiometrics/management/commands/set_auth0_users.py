from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.db.utils import IntegrityError
import requests
from dotenv import load_dotenv
import os
from api.models import CustomUser, JWKS

# Load environment variables from the .env file
load_dotenv()

token_url = f'https://{os.getenv("AUTH0_DOMAIN")}/oauth/token'
token_headers = {"content-type": "application/x-www-form-urlencoded"}
token_data = {
    "grant_type": "client_credentials",
    "client_id": f'{os.getenv("AUTH0_CLIENT_ID")}',
    "client_secret": f'{os.getenv("AUTH0_CLIENT_SECRET")}',
    "audience": f'{os.getenv("AUTH0_AUDIENCE")}',
}


class Command(BaseCommand):
    help = "Get Auth0 user"

    def handle(self, *args, **kwargs):
        # Remove all users without an auth0_id
        users = CustomUser.objects.all()
        for user in users:
            if user.auth0_id == "":
                user.delete()

        try:
            jwks_url = f'https://{os.getenv("AUTH0_DOMAIN")}/.well-known/jwks.json'
            jwks_data = requests.get(jwks_url).json()
            JWKS.objects.create(jwks=jwks_data)

            response = requests.post(token_url, headers=token_headers, data=token_data)
            token = response.json()["access_token"]
            users_url = f'https://{os.getenv("AUTH0_DOMAIN")}/api/v2/users'
            users_headers = {"Authorization": f"Bearer {token}"}
            response = requests.get(users_url, headers=users_headers)
            users = response.json()
            for user in users:
                try:
                    CustomUser.objects.create_user(
                        auth0_id=f'{user["user_id"]}',
                        email=f'{user["email"]}',
                        username=f'{user["user_id"]}',
                        nickname=f'{user["nickname"]}',
                    )
                except IntegrityError:
                    continue
        except IntegrityError:
            self.stdout.write("Default users already exist")
