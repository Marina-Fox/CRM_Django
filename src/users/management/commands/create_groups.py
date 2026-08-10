from typing import Any

from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission


class Command(BaseCommand):
    """
    Создание групп пользователей.
    """

    def handle(self, *args: Any, **options: Any) -> str | None:
        groups_data = {
            "Admins": ["view_user", "change_user", "add_user", "delete_user"],
            "Marketing": [
                "add_services",
                "change_services",
                "delete_services",
                "view_services",
                "add_advertisement",
                "change_advertisement",
                "delete_advertisement",
                "view_advertisement",
            ],
            "Operators": ["add_lead", "change_lead", "delete_lead", "view_lead"],
            "Managers": [
                "add_contracts",
                "change_contracts",
                "delete_contracts",
                "view_contracts",
                "view_lead",
                "add_customers",
                "change_customers",
                "delete_customers",
                "view_customers",
            ],
        }

        for group_name, perms_codenames in groups_data.items():
            group, _ = Group.objects.get_or_create(name=group_name)

            for codename in perms_codenames:
                perm = Permission.objects.get(codename=codename)
                group.permissions.add(perm)
