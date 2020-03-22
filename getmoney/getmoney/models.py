from django.db import models
from django.contrib.auth.models import User


class Adv(models.Model):
    owner = models.ForeignKey('auth.User', related_name='ads', on_delete=models.CASCADE)

    datetime_start = models.DateTimeField()
    datetime_end = models.DateTimeField()
    content = models.TextField(max_length=512)
    wn8 = models.IntegerField(default=0)
    wins_percent = models.IntegerField(default=0)
    url_clan = models.CharField(max_length=150)

