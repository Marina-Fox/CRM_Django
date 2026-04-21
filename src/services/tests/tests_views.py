from decimal import Decimal
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User, Permission
from django.contrib.contenttypes.models import ContentType


from ..models import Services


# Create your tests here.
class TestServicesListView(TestCase):
    """
    Тесты для представленния ServicesList.
    """

    def setUp(self) -> None:
        self.service_1 = Services.objects.create(
            title="Title",
            description="descrip",
            cost=Decimal("500.00"),
        )
        self.service_2 = Services.objects.create(
            title="Title 2",
            description="descrip 2",
            cost=Decimal("1500.00"),
        )
        self.user = User.objects.create_user(username="test_user", password="pass")
        con_type = ContentType.objects.get_for_model(Services)
        self.permis = Permission.objects.get(
            codename="view_services",
            content_type=con_type,
        )
        self.url = reverse("services:services_list")

    def test_get_services_list(self):
        "Проверка получения списка услуг."
        self.user.user_permissions.add(self.permis)
        self.client.force_login(self.user)
        respons = self.client.get(self.url)

        self.assertEqual(respons.status_code, 200)
        self.assertQuerySetEqual(
            respons.context["services"], [self.service_2, self.service_1], ordered=False
        )

    def test_get_services_list_unauthorized(self):
        "Проверка перенаправления пользователя на страницу входа."
        respons = self.client.get(self.url)
        self.assertEqual(respons.status_code, 302)
        self.assertRedirects(respons, f"/admin/login/?next={self.url}")

    def test_get_services_list_permis(self):
        "Проверка, что пользователь без разрешения view_services не может просмотреть список услуг."
        self.client.force_login(self.user)
        respons = self.client.get(self.url)

        self.assertEqual(respons.status_code, 403)


class TestServicesDetailView(TestCase):
    """
    Тесты для представленния ServicesDetail.
    """

    def setUp(self) -> None:
        self.service = Services.objects.create(
            title="Title",
            description="descrip",
            cost=Decimal("500.00"),
        )
        self.user = User.objects.create_user(username="test_user", password="pass")
        con_type = ContentType.objects.get_for_model(Services)
        self.permis = Permission.objects.get(
            codename="view_services",
            content_type=con_type,
        )
        self.url = reverse("services:services_detail", args=[self.service.pk])

    def test_get_services_detail(self):
        "Проверка получения страницы деталей услуги."
        self.user.user_permissions.add(self.permis)
        self.client.force_login(self.user)
        respons = self.client.get(self.url)

        self.assertEqual(respons.status_code, 200)
        self.assertTemplateUsed(respons, "services/services_detail.html")
        self.assertEqual(respons.context["object"], self.service)

    def test_get_services_detail_unauthorized(self):
        "Проверка перенаправления пользователя на страницу входа."
        respons = self.client.get(self.url)
        self.assertEqual(respons.status_code, 302)
        self.assertRedirects(respons, f"/admin/login/?next={self.url}")

    def test_get_services_detail_permis(self):
        "Проверка, что пользователь без разрешения view_services не может просмотреть детальную страницу услуги."
        self.client.force_login(self.user)
        respons = self.client.get(self.url)

        self.assertEqual(respons.status_code, 403)


class TestServicesCreateView(TestCase):
    """
    Тесты для представленния ServicesCreate.
    """

    def setUp(self) -> None:
        self.user = User.objects.create_user(username="test_user", password="pass")
        con_type = ContentType.objects.get_for_model(Services)
        self.permis_add = Permission.objects.get(
            codename="add_services",
            content_type=con_type,
        )
        self.permis_view = Permission.objects.get(
            codename="view_services",
            content_type=con_type,
        )
        self.url = reverse("services:services_create")

    def test_get_services_create(self):
        "Проверка получения формы для создания услуги."
        self.user.user_permissions.add(self.permis_add)
        self.client.force_login(self.user)
        respons = self.client.get(self.url)

        self.assertEqual(respons.status_code, 200)
        self.assertTemplateUsed(respons, "services/services_create.html")

    def test_post_services_create(self):
        "Проверка создания новой услуги."
        self.user.user_permissions.add(self.permis_add, self.permis_view)
        self.client.force_login(self.user)
        data = {
            "title": "Test Create",
            "description": "Test create",
            "cost": Decimal("500.00"),
        }
        respons = self.client.post(self.url, data=data, format="json")

        self.assertEqual(respons.status_code, 302)

        service = Services.objects.first()
        self.assertRedirects(
            respons, reverse("services:services_detail", args=[service.pk])
        )

    def test_get_services_create_unauthorized(self):
        "Проверка перенаправления пользователя на страницу входа."
        respons = self.client.get(self.url)
        self.assertEqual(respons.status_code, 302)
        self.assertRedirects(respons, f"/admin/login/?next={self.url}")

    def test_get_services_creat_permis(self):
        "Проверка, что пользователь без разрешения add_services не может создать новую услугу."
        self.client.force_login(self.user)
        respons = self.client.get(self.url)

        self.assertEqual(respons.status_code, 403)


class TestServicesUpdateView(TestCase):
    """
    Тесты для представленния ServicesUpdate.
    """

    def setUp(self) -> None:
        self.service = Services.objects.create(
            title="Title",
            description="descrip",
            cost=Decimal("500.00"),
        )
        self.user = User.objects.create_user(username="test_user", password="pass")
        con_type = ContentType.objects.get_for_model(Services)
        self.permis_update = Permission.objects.get(
            codename="change_services",
            content_type=con_type,
        )
        self.permis_view = Permission.objects.get(
            codename="view_services",
            content_type=con_type,
        )
        self.url = reverse("services:services_update", args=[self.service.pk])

    def test_get_services_update(self):
        "Проверка получения формы для обновления услуги."
        self.user.user_permissions.add(self.permis_update)
        self.client.force_login(self.user)
        respons = self.client.get(self.url)

        self.assertEqual(respons.status_code, 200)
        self.assertTemplateUsed(respons, "services/services_edit.html")

    def test_post_services_update(self):
        "Проверка внесения изменений в услугу."
        self.user.user_permissions.add(self.permis_update, self.permis_view)
        self.client.force_login(self.user)
        data = {
            "title": "Test Update",
            "description": "Test update",
            "cost": Decimal("50.00"),
        }
        respons = self.client.post(self.url, data=data, format="json")

        self.assertEqual(respons.status_code, 302)

        service = Services.objects.first()
        self.assertRedirects(
            respons, reverse("services:services_detail", args=[service.pk])
        )

    def test_get_services_update_unauthorized(self):
        "Проверка перенаправления пользователя на страницу входа."
        respons = self.client.get(self.url)
        self.assertEqual(respons.status_code, 302)
        self.assertRedirects(respons, f"/admin/login/?next={self.url}")

    def test_get_services_update_permis(self):
        "Проверка, что пользователь без разрешения change_services не может изменить услугу."
        self.client.force_login(self.user)
        respons = self.client.get(self.url)

        self.assertEqual(respons.status_code, 403)


class TestServicesDeleteView(TestCase):
    """
    Тесты для представленния ServicesDelete.
    """

    def setUp(self) -> None:
        self.service = Services.objects.create(
            title="Title",
            description="descrip",
            cost=Decimal("500.00"),
        )
        self.user = User.objects.create_user(username="test_user", password="pass")
        con_type = ContentType.objects.get_for_model(Services)
        self.permis_del = Permission.objects.get(
            codename="delete_services",
            content_type=con_type,
        )
        self.permis_view = Permission.objects.get(
            codename="view_services",
            content_type=con_type,
        )
        self.url = reverse("services:services_delete", args=[self.service.pk])

    def test_get_services_delete(self):
        "Проверка получения формы для удаления услуги."
        self.user.user_permissions.add(self.permis_del)
        self.client.force_login(self.user)
        respons = self.client.get(self.url)

        self.assertEqual(respons.status_code, 200)
        self.assertTemplateUsed(respons, "services/services_delete.html")

    def test_delete_services(self):
        "Проверка удаления услуги."
        self.user.user_permissions.add(self.permis_del, self.permis_view)
        self.client.force_login(self.user)
        respons = self.client.delete(self.url)

        self.assertEqual(respons.status_code, 302)
        self.assertRedirects(respons, reverse("services:services_list"))

    def test_get_services_delete_unauthorized(self):
        "Проверка перенаправления пользователя на страницу входа."
        respons = self.client.get(self.url)
        self.assertEqual(respons.status_code, 302)
        self.assertRedirects(respons, f"/admin/login/?next={self.url}")

    def test_get_services_delete_permis(self):
        "Проверка, что пользователь без разрешения delete_services не может удалить услугу."
        self.client.force_login(self.user)
        respons = self.client.get(self.url)

        self.assertEqual(respons.status_code, 403)
