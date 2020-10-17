"""Suscription views."""

# Django
from django.shortcuts import render, redirect

# Models
from .models import Suscription, Plan

# Utils
import datetime

# Create your views here.


def suscription_validate(request):
    try:
        request.session["suscription"] = request.GET["suscription"]
    except:
        pass
    user_id = request.user.id
    free_plan_id = 1
    if "suscription" in request.session:
        plan_id = int(request.session["suscription"])
        if plan_id == 0:
            return redirect("user_oportunities")
        suscriptions = Suscription.objects.filter(user=user_id).values("plan", "active")
        # Check if the user has had plans
        if suscriptions.count() == 0:
            # Check if require activate free plan
            if plan_id == free_plan_id:
                create_plan(user_id, plan_id, datetime.datetime.today())
                request.session["suscription"] = 0
                title = "Gracias por registrarse"
                message = "Su suscripción gratuita por 30 días ha sido activada."
                detail = "Ya puede empezar a disfrutar de su suscripción con "
                return render(
                    request,
                    "suscriptions/registered_suscription.html",
                    {"title": title, "message": message, "detail": detail},
                )
            # Check if require activate other plan and plan free
            else:
                create_plan(user_id, free_plan_id, datetime.datetime.today())
                # TODO: Validate payment
                create_plan(
                    user_id,
                    plan_id,
                    datetime.datetime.today() + datetime.timedelta(days=32),
                )
                request.session["suscription"] = 0
                title = "Gracias por registrarse"
                message = "Su suscripción ha sido activada. Adicionalmente su suscripción tendrá 30 días adicionales totalmente gratis."
                detail = "Ya puede empezar a disfrutar de su suscripción con "
                return render(
                    request,
                    "suscriptions/registered_suscription.html",
                    {"title": title, "message": message, "detail": detail},
                )
        else:
            suscriptions = (
                Suscription.objects.filter(user=user_id, active=True)
                .values_list("end_date", flat=True)
                .order_by("-end_date")
            )
            if plan_id != free_plan_id:
                # Check if user has active plan
                if suscriptions.count() > 0:
                    # TODO: Validate payment
                    create_plan(
                        user_id, plan_id, suscriptions[0] + datetime.timedelta(days=1)
                    )
                    request.session["suscription"] = 0
                    title = "Gracias por renovar su suscripción"
                    message = "Su suscripción será activada cuando su suscripción actual culmine."
                    detail = (
                        "Por lo pronto, puede sergir disfrutando su suscripción con "
                    )
                    return render(
                        request,
                        "suscriptions/registered_suscription.html",
                        {"title": title, "message": message, "detail": detail},
                    )
                else:
                    # Create a new plan if the user has no active plans and has already used the free plan
                    create_plan(user_id, plan_id, datetime.datetime.today())
                    request.session["suscription"] = 0
                    title = "Gracias por registrarse"
                    message = "Su suscripción ha sido activada."
                    detail = "Ya puede empezar a disfrutar de su suscripción con "
                    return render(
                        request,
                        "suscriptions/registered_suscription.html",
                        {"title": title, "message": message, "detail": detail},
                    )
            else:
                free_suscription = Suscription.objects.filter(
                    plan_id=free_plan_id, active=True
                ).values_list("id", flat=True)
                if free_suscription.count() == 0:
                    title = "Su suscripción gratuita ya ha finalizado"
                    message = "Adquiera el plan que más se ajuste a las necesidades de su empresa."
                    detail = "Estaremos atentos a sus inquietudes y sugerencias."
                    return render(
                        request,
                        "suscriptions/registered_suscription_plans.html",
                        {"title": title, "message": message, "detail": detail},
                    )
                else:
                    title = "Su suscripción gratuita ya ha sido activada"
                    message = ""
                    detail = ""
                    return render(
                        request,
                        "suscriptions/registered_suscription.html",
                        {"title": title, "message": message, "detail": detail},
                    )
    else:
        suscriptions = Suscription.objects.filter(user=user_id, active=True).values(
            "plan"
        )
        # Check if the user has had plans
        if suscriptions.count() == 0:
            title = "Usted no cuenta con una suscripción activa"
            message = (
                "Adquiera el plan que más se ajuste a las necesidades de su empresa."
            )
            detail = "Estaremos atentos a sus inquietudes y sugerencias."
            return render(
                request,
                "suscriptions/registered_suscription_plans.html",
                {"title": title, "message": message, "detail": detail},
            )
        else:
            return redirect("user_oportunities")


def create_plan(user_id, plan_id, start_date):
    plan = Plan.objects.filter(id=plan_id).values_list("days", flat=True)
    suscription = Suscription(
        user_id=user_id,
        plan_id=plan_id,
        active=True,
        start_date=start_date,
        end_date=(start_date + datetime.timedelta(days=plan[0])),
    )
    suscription.save()