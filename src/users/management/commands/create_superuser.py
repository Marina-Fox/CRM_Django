import os

from dotenv import load_dotenv
from typing import Any

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError


load_dotenv(dotenv_path=".env.superuser")


class Command(BaseCommand):
    """
    Создание суперпользователя.
    """

    def handle(self, *args: Any, **options: Any) -> str | None:
        User = get_user_model()

        username = os.getenv("DJANGO_SUPERUSER_USERNAME")
        password = os.getenv("DJANGO_SUPERUSER_PASSWORD")

        if not username:
            raise CommandError("DJANGO_SUPERUSER_USERNAME не определен")

        if not password:
            raise CommandError("DJANGO_SUPERUSER_PASSWORD не определен")

        user = User.objects.filter(username=username).first()

        if user:
            if not user.is_superuser or not user.is_staff:
                user.is_superuser = True
                user.is_staff = True
                user.save(update_fields=["is_superuser", "is_staff"])

            return

        user_data = {
            User.USERNAME_FIELD: username,
        }

        user = User.objects.create_superuser(password=password, **user_data)
