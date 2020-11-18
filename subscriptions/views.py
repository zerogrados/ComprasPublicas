"""Subscription views."""

# Django
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt

# Models
from .models import Subscription, Plan
from django.contrib.sites.models import Site

# Utils
import datetime

# Create your views here.


def create_plan(user_id, plan_id, start_date, payment_detail=None):
    plan = Plan.objects.filter(id=plan_id).values_list("days", flat=True)
    subscription = Subscription(
        user_id=user_id,
        plan_id=plan_id,
        active=True,
        start_date=start_date,
        end_date=(start_date + datetime.timedelta(days=plan[0])),
        payment_detail = payment_detail
    )
    subscription.save()

def subscription_validate(request):
    user_id = request.user.id
    free_plan_id = 1
    domain = Site.objects.get_current().domain
    if "subscription" in request.session:
        plan_id = int(request.session["subscription"])
        if plan_id == 0:
            return redirect("user_oportunities")
        subscriptions = Subscription.objects.filter(user=user_id).values("plan", "active")
        # Check if the user has had plans
        if subscriptions.count() == 0:
            # Check if require activate free plan
            if plan_id == free_plan_id:
                create_plan(user_id, plan_id, datetime.datetime.today())
                request.session["subscription"] = 0
                title = "Gracias por registrarse"
                message = "Su suscripción gratuita por 30 días ha sido activada. Adquiera el plan que más se ajuste a sus necesidades."
                detail = "Ya puede empezar a disfrutar de su suscripción."
                return render(
                    request,
                    "subscriptions/registered_subscription_plans.html",
                    {"title": title, "message": message, "detail": detail, "user_id": user_id, "domain": domain,},
                )
            # Check if require activate other plan and plan free
            else:
                title = "Gracias por registrarse"
                message = "Adquiera el plan que más se ajuste a las necesidades de su empresa."
                detail = "Estamos atentos a sus inquietudes y sugerencias."
                user_id = request.user.id
                return render(
                    request,
                    "subscriptions/registered_subscription_plans.html",
                    {"title": title, "message": message, "detail": detail, "user_id": user_id, "domain": domain,},
                )                
        else:
            subscriptions = (
                Subscription.objects.filter(user=user_id, active=True)
                .values_list("end_date", flat=True)
                .order_by("-end_date")
            )
            if plan_id != free_plan_id:
                # Check if user has active plan
                if subscriptions.count() > 0:
                    request.session["subscription"] = 0
                    title = "Adquiera el plan que más se ajuste a las necesidades de su empresa."
                    message = "Su suscripción será activada cuando su suscripción actual culmine."
                    detail = (
                        ""
                    )
                    return render(
                        request,
                        "subscriptions/registered_subscription_plans.html",
                        {"title": title, "message": message, "detail": detail, "user_id": user_id, "domain": domain,},
                    )
                else:
                    # Create a new plan if the user has no active plans and has already used the free plan
                    request.session["subscription"] = 0
                    title = "Adquiera el plan que más se ajuste a las necesidades de su empresa."
                    message = ""
                    detail = "Estamos atentos a sus inquietudes y sugerencias."
                    return render(
                        request,
                        "subscriptions/registered_subscription_plans.html",
                        {"title": title, "message": message, "detail": detail, "user_id": user_id, "domain": domain,},
                    )
            else:
                free_subscription = Subscription.objects.filter(
                    plan_id=free_plan_id, active=True
                ).values_list("id", flat=True)
                if free_subscription.count() == 0:
                    title = "Su suscripción gratuita ya ha finalizado"
                    message = "Adquiera el plan que más se ajuste a las necesidades de su empresa."
                    detail = "Estamos atentos a sus inquietudes y sugerencias."
                    return render(
                        request,
                        "subscriptions/registered_subscription_plans.html",
                        {"title": title, "message": message, "detail": detail, "domain": domain,},
                    )
                else:
                    title = "Su suscripción gratuita ya ha sido activada"
                    message = "Adquiera el plan que más se ajuste a las necesidades de su empresa."
                    detail = "Estamos atentos a sus inquietudes y sugerencias."
                    return render(
                        request,
                        "subscriptions/registered_subscription_plans.html",
                        {"title": title, "message": message, "detail": detail, "user_id": user_id, "domain": domain,},
                    )
    else:
        subscriptions = Subscription.objects.filter(user=user_id, active=True).values(
            "plan"
        )
        # Check if the user has had plans
        if subscriptions.count() == 0:
            title = "Usted no cuenta con una suscripción activa"
            message = (
                "Adquiera el plan que más se ajuste a las necesidades de su empresa."
            )
            detail = "Estamos atentos a sus inquietudes y sugerencias."
            return render(
                request,
                "subscriptions/registered_subscription_plans.html",
                {"title": title, "message": message, "detail": detail, "user_id": user_id, "domain": domain,},
            )
        else:
            return redirect("user_oportunities")
@csrf_exempt
def payment_response(request):
    free_plan_id = 1
    if request.POST:
        request.session["subscription"] = request.POST['x_extra1']
        request.session["user_id"] = request.POST['x_extra2']
        if request.POST['x_response'] == 'Aceptada':
            user_id = request.session["user_id"]
            subsciption_validate = Subscription.objects.filter(payment_detail__x_ref_payco=request.POST['x_ref_payco']).values_list('id', flat=True)
            if subsciption_validate:
                return redirect("user_oportunities")
            if "subscription" in request.session:
                plan_id = int(request.POST['x_extra1'])
                if plan_id == 0:
                    return redirect("user_oportunities")
                subscriptions = Subscription.objects.filter(user=user_id).values("plan", "active")
                # Check if the user has had plans
                if subscriptions.count() == 0:
                    # Check if require activate free plan
                    if plan_id == free_plan_id:
                        create_plan(user_id, plan_id, datetime.datetime.today())
                        request.session["subscription"] = 0
                        title = "Gracias por registrarse"
                        message = "Su suscripción gratuita por 30 días ha sido activada."
                        detail = "Ya puede empezar a disfrutar de su suscripción con "
                        return render(
                            request,
                            "subscriptions/registered_subscription.html",
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
                            request.POST
                        )
                        title = "Transacción aprobada"
                        message = "Su suscripción ha sido activada. Adicionalmente su suscripción tendrá 30 días adicionales totalmente gratis."
                        detail = "Ya puede empezar a disfrutar de su suscripción con "
                        return render(
                            request,
                            "subscriptions/registered_subscription.html",
                            {"title": title, "message": message, "detail": detail},
                        )
                else:
                    subscriptions = (
                        Subscription.objects.filter(user=user_id, active=True)
                        .values_list("end_date", flat=True)
                        .order_by("-end_date")
                    )
                    if plan_id != free_plan_id:
                        # Check if user has active plan
                        if subscriptions.count() > 0:
                            # TODO: Validate payment
                            create_plan(
                                user_id, plan_id, subscriptions[0] + datetime.timedelta(days=1), request.POST
                            )
                            request.session["subscription"] = 0
                            title = "Gracias por renovar su suscripción"
                            message = "Su suscripción será activada cuando su suscripción actual culmine."
                            detail = (
                                "Por lo pronto, puede sergir disfrutando su suscripción con "
                            )
                            return render(
                                request,
                                "subscriptions/registered_subscription.html",
                                {"title": title, "message": message, "detail": detail},
                            )
                        else:
                            # Create a new plan if the user has no active plans and has already used the free plan
                            create_plan(user_id, plan_id, datetime.datetime.today(), request.POST)
                            request.session["subscription"] = 0
                            title = "Transacción aprobada"
                            message = "Su suscripción ha sido activada."
                            detail = "Ya puede empezar a disfrutar de su suscripción con "
                            return render(
                                request,
                                "subscriptions/registered_subscription.html",
                                {"title": title, "message": message, "detail": detail},
                            )
                    else:
                        free_subscription = Subscription.objects.filter(
                            plan_id=free_plan_id, active=True
                        ).values_list("id", flat=True)
                        if free_subscription.count() == 0:
                            title = "Su suscripción gratuita ya ha finalizado"
                            message = "Adquiera el plan que más se ajuste a las necesidades de su empresa."
                            detail = "Estamos atentos a sus inquietudes y sugerencias."
                            return render(
                                request,
                                "subscriptions/registered_subscription_plans.html",
                                {"title": title, "message": message, "detail": detail, "domain": domain,},
                            )
                        else:
                            title = "Su suscripción gratuita ya ha sido activada"
                            message = "Adquiera el plan que más se ajuste a las necesidades de su empresa."
                            detail = "Estamos atentos a sus inquietudes y sugerencias."
                            return render(
                                request,
                                "subscriptions/registered_subscription.html",
                                {"title": title, "message": message, "detail": detail, "user_id": user_id},
                            )
            else:
                subscriptions = Subscription.objects.filter(user=user_id, active=True).values(
                    "plan"
                )
                # Check if the user has had plans
                if subscriptions.count() == 0:
                    title = "Usted no cuenta con una suscripción activa"
                    message = (
                        "Adquiera el plan que más se ajuste a las necesidades de su empresa."
                    )
                    detail = "Estamos atentos a sus inquietudes y sugerencias."
                    return render(
                        request,
                        "subscriptions/registered_subscription_plans.html",
                        {"title": title, "message": message, "detail": detail, "domain": domain,},
                    )
                else:
                    return redirect("user_oportunities")
        if request.POST['x_response'] == 'Rechazada':
            title = "Su transacción ha sido rechazada"
            message = "Por favor revise su pago he intentelo de nuevo. Estamos atentos a sus inquietudes y sugerencias."
            detail = ""
            return render(
                request,
                "subscriptions/registered_subscription_response.html",
                {"title": title, "message": message, "detail": detail},
            )
        if request.POST['x_response'] == 'Pendiente':
            title = "Su transacción se encuentra en estado pendiente"
            message = "Por favor revise su pago he intentelo de nuevo. Estamos atentos a sus inquietudes y sugerencias."
            detail = ""
            return render(
                request,
                "subscriptions/registered_subscription_response.html",
                {"title": title, "message": message, "detail": detail},
            )            
    else:
        if request.user.is_authenticated:
            pass
        else:
            return redirect("home_page")