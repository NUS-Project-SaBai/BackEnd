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
            users_url = f'https://{os.getenv("AUTH0_DOMAIN")}/api/v2/users?include_totals=true&page='

            # AUTH0 limits the number of users retured
            # TODO: PROPER EXPORT: https://auth0.com/docs/manage-users/user-migration/bulk-user-exports
            users_headers = {"Authorization": f"Bearer {token}"}
            users = []
            for curPage in range(0, 20):
                response = requests.get(users_url + str(curPage), headers=users_headers)
                users.extend(response.json()["users"])
                if len(response.json()["users"]) < 50:
                    break
            auth0_ids = set(user["user_id"] for user in users)

            for user in users:
                db_user, is_created = CustomUser.objects.get_or_create(
                    auth0_id=user["user_id"],
                    defaults={
                        "email": user["email"],
                        "username": user["username"],
                        "nickname": user["nickname"],
                        "role": user.get("user_metadata", {}).get("role", "member"),
                    },
                )
                if not is_created:
                    db_user.email = user["email"]
                    db_user.username = user["username"]
                    db_user.nickname = user["nickname"]
                    db_user.role = user.get("user_metadata", {}).get("role", "member")
                    db_user.save()

            for user in CustomUser.objects.all():
                if user.auth0_id not in auth0_ids:
                    user.delete()
        except IntegrityError:
            self.stdout.write("Default users already exist")
