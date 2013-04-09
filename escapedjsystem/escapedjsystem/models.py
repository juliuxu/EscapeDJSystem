from django.db import models


class Song(models.Model):
    text = models.CharField(max_length=100)
    date = models.DateTimeField(auto_now_add=True)


class SongRequest(models.Model):
    song = models.ForeignKey(Song)
    date = models.DateTimeField(auto_now_add=True)
    played = models.BooleanField(default=False)


class Message(models.Model):
    text = models.CharField(max_length=320)
    date = models.DateTimeField(auto_now_add=True)
    seen = models.BooleanField(default=False)
