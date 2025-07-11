from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

User = get_user_model()


def list_users():
    return User.objects.all()


def get_user(pk):
    return get_object_or_404(User, pk=pk)


def create_user(validated_data):
    return User.objects.create(**validated_data)


def update_user(user, validated_data):
    for attr, value in validated_data.items():
        setattr(user, attr, value)
    user.save()
    return user


def delete_user(user):
    user.delete()
