"""Profile middleware."""

# Django
from django.shortcuts import redirect
from django.urls import reverse


class ProfileCompletionMiddleware:
    """Profile completion middleware

    Ensure every user that is interacting with the platform
    have their profile nom_empresa, nit, telefono, ciudades,
    presupuesto_min, presupuesto_max and activ_economica.
    """

    def __init__(self, get_response):
        """Middleware initialization."""
        self.get_response = get_response

    def __call__(self, request):
        """Code to be executed for each request before the view is called."""
        if not request.user.is_anonymous:
            if not request.user.is_staff:
                profile = request.user.perfil
                if (
                    not profile.nom_empresa
                    or not profile.nit
                    or not profile.telefono
                    or not profile.ciudades
                    or not profile.presupuesto_min
                    or not profile.presupuesto_max
                    or not profile.activ_economica
                ):
                    if request.path not in [
                        reverse("enterprise_profile"),
                        reverse("cerrar_sesion"),
                        reverse("home_page"),
                        reverse("contact_page"),
                        reverse("welcome_page"),
                    ]:
                        return redirect("enterprise_profile")

        response = self.get_response(request)
        return response
