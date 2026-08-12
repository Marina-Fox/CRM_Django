from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView


class CustomLoginView(LoginView):
    """
    Авторизация пользователей.
    """

    template_name = "users/login.html"

    def get_success_url(self) -> str:
        if (
            self.request.user.groups.filter(name="Admins").exists()
            or self.request.user.is_superuser
        ):
            return reverse_lazy("admin:index")

        return reverse_lazy("home")
