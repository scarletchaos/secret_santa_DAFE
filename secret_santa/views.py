from django.http import HttpResponse
from secret_santa.models import User
from secret_santa.admin import assign_givers
import json

def delete_user(request):
    id = request.POST["id"]
    user = User.objects.get(id=id)
    giver = User.objects.get(gifts_to=id)
    receiver = User.objects.get(id=user.gifts_to)
    print(giver, receiver)
    User.objects.filter(id=receiver.id).update(has_giver=False)
    User.objects.filter(id=giver.id).update(gifts_to=None)
    user.delete()
    assign_givers()
    return HttpResponse(200)

def add_user(request):
    data = json.loads(request.POST)
    User.objects.create(
            id=data.get("id"),
            telegram_id=data.get("telegram_id"),
            wishes=data.get("wishes"),
            room=data.get("room", None),
            year=data.get("year", None),
            name=data.get("name")
            )
    return HttpResponse(200)

