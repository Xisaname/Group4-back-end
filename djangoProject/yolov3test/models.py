# models.py
from django.db import models


class Image(models.Model):
    imageid = models.AutoField(auto_created=True, primary_key=True)
    imageurl = models.CharField(max_length=255)
    userid = models.IntegerField()
    send_timstamp = models.CharField(max_length=255)
