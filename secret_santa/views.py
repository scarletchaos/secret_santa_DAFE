from random import randint, shuffle

from django.db.models import (Case, ExpressionWrapper, F, IntegerField, Sum,
                              Value, When)
from django.db.models.functions import Abs
from django.db.models.functions.comparison import Coalesce
from django.http import HttpResponse
from django.shortcuts import render

from secret_santa.models import User

def reset_givers(request):
    User.object.all().update(has_giver=False, gifts_to=None)
    return HttpResponse(200)

def assign_givers(request):
    users = User.objects.filter(gifts_to=None)
    user_ids = list(users.values_list("id", flat=True))
    for id in user_ids:
        user = users.get(id=id)
        free_users = User.objects.exclude(id=user.id)\
                .exclude(has_giver=True)\
                .annotate(
            priority=ExpressionWrapper(
                Sum(
                    Case(
                        When(room=user.room, then=Value(0)),
                        default=Value(10),
                        output_field=IntegerField(),
                    ) +
                    Coalesce(Abs(F('year') - user.year), 0),
                    output_field=IntegerField(),
                ),
                output_field=IntegerField(),
            )).order_by("-priority")
        selected_user = free_users.first()

        print(user, " ", user.room, " ", user.year)
        print(free_users.values("name", "surname", "room", "year", "priority", "has_giver"))
        print(selected_user, " ", selected_user.room, " ", selected_user.year)
        print()
        user.gifts_to = selected_user.id
        user.current_priority = selected_user.priority
        user.save()
        selected_user.has_giver = True
        selected_user.save()

    return HttpResponse()

def delete_user(request, id):
    user = User.objects.get(id=id)
    giver = User.objects.get(gifts_to=id)
    receiver = User.objects.get(id=user.gifts_to)
    



# Create your views here.
