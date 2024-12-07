from django.core.management.base import BaseCommand
from api.models import CustomUser,Patient


class Command(BaseCommand):
    help = "Create default users"

    # def handle(self, *args, **kwargs):
    #     users = CustomUser.objects.all()
    #     for user in users:
    #         print(user, user.auth0_id, user.nickname, user.email, user.username)
    #         if user.auth0_id == "":
    #             print("Nothing")
    #             user.delete()
        # CustomUser.objects.get(username="auth0|6728d7e3968d11339f572c66").delete()

    def handle(self, *args, **kwargs):
        patient = Patient.objects.get(id=179)
        print(patient.name)
        patient.delete()
