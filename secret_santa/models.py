from django.db import models


class User(models.Model):
    id = models.AutoField(primary_key=True)
    telegram_id = models.PositiveIntegerField(unique=True, blank=True, null=True)
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    wishes = models.CharField(max_length=100)
    room = models.PositiveIntegerField(null=True, blank=True)
    year = models.PositiveIntegerField(null=True, blank=True)
    gifts_to = models.IntegerField(null=True, unique=True, blank=True)
    has_giver = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.name} {self.surname}"
# Create your models here.
