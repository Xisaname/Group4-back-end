from django.db import models


class Image(models.Model):
    imageid = models.AutoField(auto_created=True, primary_key=True)
    imageurl = models.CharField(max_length=255)
    userid = models.IntegerField()
    send_timstamp = models.CharField(max_length=255)


class User(models.Model):
    userid = models.AutoField(auto_created=True, primary_key=True)
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)

