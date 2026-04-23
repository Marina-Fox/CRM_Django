from decimal import Decimal

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User, Permission
from django.contrib.contenttypes.models import ContentType

from ..models import Lead
from ...ad_campaign.models import Advertisement
from ...services.models import Services


class TestLeadList(TestCase):
    """
    Тесты для представленния LeadList.
    """

    def setUp(self) -> None:
        self.service = Services.objects.create(
            title="Title",
            description="descrip",
            cost=Decimal("500.00"),
        )
        self.ad_campaign = Advertisement.objects.create(
            title="Test ad camp",
            service=self.service,
            promotion_channel="Test 1",
            budget=Decimal("500.00"),
        )
        self.lead_1 = Lead.objects.create(
            first_name="Test Name",
            last_name="Test Last Name",
            patronymic="Test Patron",
            phone="+79456542656",
            email="test@mail.com",
            advertisement=self.ad_campaign,
        )
        self.lead_2 = Lead.objects.create(
            first_name="Test Name2",
            last_name="Test Last Name2",
            patronymic="Test Patron2",
            phone="+79456542655",
            email="test2@mail.com",
            advertisement=self.ad_campaign,
        )
        self.user = User.objects.create_user(username="test_user", password="pass")
        con_type = ContentType.objects.get_for_model(Lead)
        self.permis = Permission.objects.get(
            codename="view_lead",
            content_type=con_type,
        )
        self.url = reverse("clients:clients_list")

    def test_get_lead_list(self):
        "Проверка получения списка потенциальных клиентов."
        self.user.user_permissions.add(self.permis)
        self.client.force_login(self.user)
        respons = self.client.get(self.url)

        self.assertEqual(respons.status_code, 200)
        self.assertQuerySetEqual(
            respons.context["leads"],
            [self.lead_1, self.lead_2],
            ordered=False,
        )

    def test_get_lead_list_unauthorized(self):
        "Проверка перенаправления пользователя на страницу входа."
        respons = self.client.get(self.url)

        self.assertEqual(respons.status_code, 302)
        self.assertRedirects(respons, f"/admin/login/?next={self.url}")

    def test_get_lead_list_permis(self):
        "Проверка, что пользователь без разрешения view_lead не может просмотреть список потенциальных клиентов."
        self.client.force_login(self.user)
        respons = self.client.get(self.url)

        self.assertEqual(respons.status_code, 403)


class TestLeadDetail(TestCase):
    """
    Тесты для представленния LeadList.
    """

    def setUp(self) -> None:
        self.service = Services.objects.create(
            title="Title",
            description="descrip",
            cost=Decimal("500.00"),
        )
        self.ad_campaign = Advertisement.objects.create(
            title="Test ad camp",
            service=self.service,
            promotion_channel="Test 1",
            budget=Decimal("500.00"),
        )
        self.lead = Lead.objects.create(
            first_name="Test Name",
            last_name="Test Last Name",
            patronymic="Test Patron",
            phone="+79456542656",
            email="test@mail.com",
            advertisement=self.ad_campaign,
        )
        self.user = User.objects.create_user(username="test_user", password="pass")
        con_type = ContentType.objects.get_for_model(Lead)
        self.permis = Permission.objects.get(
            codename="view_lead",
            content_type=con_type,
        )
        self.url = reverse("clients:clients_detail", args=[self.lead.pk])

    def test_get_lead_detail(self):
        "Проверка получения страницы деталей потенциального клиента."
        self.user.user_permissions.add(self.permis)
        self.client.force_login(self.user)
        respons = self.client.get(self.url)

        self.assertEqual(respons.status_code, 200)
        self.assertTemplateUsed(respons, "clients/leads_detail.html")
        self.assertEqual(respons.context["object"], self.lead)

    def test_get_lead_list_unauthorized(self):
        "Проверка перенаправления пользователя на страницу входа."
        respons = self.client.get(self.url)

        self.assertEqual(respons.status_code, 302)
        self.assertRedirects(respons, f"/admin/login/?next={self.url}")

    def test_get_lead_list_permis(self):
        "Проверка, что пользователь без разрешения view_lead не может просмотреть детали потенциального клиента."
        self.client.force_login(self.user)
        respons = self.client.get(self.url)

        self.assertEqual(respons.status_code, 403)


class TestLeadCreate(TestCase):
    """
    Тесты для представленния LeadCreate.
    """

    def setUp(self) -> None:
        self.service = Services.objects.create(
            title="Title",
            description="descrip",
            cost=Decimal("500.00"),
        )
        self.ad_campaign = Advertisement.objects.create(
            title="Test ad camp",
            service=self.service,
            promotion_channel="Test 1",
            budget=Decimal("500.00"),
        )
        self.user = User.objects.create_user(username="test_user", password="pass")
        con_type = ContentType.objects.get_for_model(Lead)
        self.permis_view = Permission.objects.get(
            codename="view_lead",
            content_type=con_type,
        )
        self.permis_add = Permission.objects.get(
            codename="add_lead",
            content_type=con_type,
        )
        self.url = reverse("clients:clients_create")

    def test_get_lead_create(self):
        "Проверка получения формы для добавления потенциального клиента."
        self.user.user_permissions.add(self.permis_add)
        self.client.force_login(self.user)
        respons = self.client.get(self.url)

        self.assertEqual(respons.status_code, 200)
        self.assertTemplateUsed(respons, "clients/leads_create.html")

    def test_post_lead_create(self):
        "Проверка добавления нового потенциального клиента."
        self.user.user_permissions.add(self.permis_add, self.permis_view)
        self.client.force_login(self.user)
        data = {
            "first_name": "Test Name",
            "last_name": "Test Last Name",
            "patronymic": "Test Patron",
            "phone": "+79456542656",
            "email": "test@mail.com",
            "advertisement": self.ad_campaign.pk,
        }
        respons = self.client.post(self.url, data=data, format="json")

        self.assertEqual(respons.status_code, 302)

        lead = Lead.objects.first()
        self.assertRedirects(respons, reverse("clients:clients_detail", args=[lead.pk]))

    def test_get_lead_create_unauthorized(self):
        "Проверка перенаправления пользователя на страницу входа."
        respons = self.client.get(self.url)
        self.assertEqual(respons.status_code, 302)
        self.assertRedirects(respons, f"/admin/login/?next={self.url}")

    def test_get_lead_creat_permis(self):
        "Проверка, что пользователь без разрешения add_lead не может добавить нового потенциального клиента."
        self.client.force_login(self.user)
        respons = self.client.get(self.url)

        self.assertEqual(respons.status_code, 403)


class TestLeadUpdate(TestCase):
    """
    Тесты для представленния LeadUpdate.
    """

    def setUp(self) -> None:
        self.service = Services.objects.create(
            title="Title",
            description="descrip",
            cost=Decimal("500.00"),
        )
        self.ad_campaign = Advertisement.objects.create(
            title="Test ad camp",
            service=self.service,
            promotion_channel="Test 1",
            budget=Decimal("500.00"),
        )
        self.lead = Lead.objects.create(
            first_name="Test Name",
            last_name="Test Last Name",
            patronymic="Test Patron",
            phone="+79456542656",
            email="test@mail.com",
            advertisement=self.ad_campaign,
        )
        self.user = User.objects.create_user(username="test_user", password="pass")
        con_type = ContentType.objects.get_for_model(Lead)
        self.permis_view = Permission.objects.get(
            codename="view_lead",
            content_type=con_type,
        )
        self.permis_update = Permission.objects.get(
            codename="change_lead",
            content_type=con_type,
        )
        self.url = reverse("clients:client_update", args=[self.lead.pk])

    def test_get_lead_update(self):
        "Проверка получения формы для редактирования информации о потенциальном клиенте."
        self.user.user_permissions.add(self.permis_update)
        self.client.force_login(self.user)
        respons = self.client.get(self.url)

        self.assertEqual(respons.status_code, 200)
        self.assertTemplateUsed(respons, "clients/leads_edit.html")

    def test_post_lead_update(self):
        "Проверка редактирования информации о потенциальном клиенте."
        self.user.user_permissions.add(self.permis_update, self.permis_view)
        self.client.force_login(self.user)
        data = {
            "first_name": "New Name",
            "last_name": "Test Last Name",
            "patronymic": "Test Patron",
            "phone": "+79456542656",
            "email": "test@mail.com",
            "advertisement": self.ad_campaign.pk,
        }
        respons = self.client.post(self.url, data=data, format="json")
        self.assertEqual(respons.status_code, 302)

        lead = Lead.objects.first()
        self.assertRedirects(respons, reverse("clients:clients_detail", args=[lead.pk]))

    def test_get_lead_list_unauthorized(self):
        "Проверка перенаправления пользователя на страницу входа."
        respons = self.client.get(self.url)

        self.assertEqual(respons.status_code, 302)
        self.assertRedirects(respons, f"/admin/login/?next={self.url}")

    def test_get_lead_list_permis(self):
        "Проверка, что пользователь без разрешения change_lead не может изменить информацию у потенциального клиента."
        self.client.force_login(self.user)
        respons = self.client.get(self.url)

        self.assertEqual(respons.status_code, 403)
