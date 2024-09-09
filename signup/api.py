import json
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.http import JsonResponse
from django.contrib.auth import login
from signup.forms import SignUpForm


class SignUpView(APIView):

    def post(self, request):
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')
        if not (username and password):
            return JsonResponse({"status": "error", "errors": {"username": "This field is required.", "password": "This field is required."}}, status=400)
        form = SignUpForm(data)
        if form.is_valid():
            user = form.save()
            login(request, user)
            refresh = RefreshToken.for_user(user)
            return JsonResponse({"user": {"id": user.id, "username": user.username, }, "access": str(refresh.access_token)}, status=201)
        else:
            return JsonResponse(form.errors, status=400)
