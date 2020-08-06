from django.db import models


# Create your models here.
class Vtuber(models.Model):
    name = models.CharField(max_length=128,primary_key=True)
    bilibili_uid = models.IntegerField()
    youtube_id = models.CharField(max_length=128)
    twitter_id = models.CharField(max_length=128, default='')


class VoiceGroup(models.Model):
    vtb_name = models.CharField(max_length=128)
    group_name = models.CharField(max_length=128)
    all_count = models.IntegerField()
    translate = models.TextField(default='')


class Voice(models.Model):
    vtb_name = models.CharField(max_length=128)
    name = models.CharField(max_length=128)
    group = models.CharField(max_length=128)
    url = models.URLField()
    version = models.CharField(max_length=20)
    count = models.IntegerField()
    update_time = models.DateTimeField(auto_now=True)
    translate = models.TextField()
    tag = models.CharField(max_length=32, default='')


class Translate(models.Model):
    name = models.CharField(max_length=128)
    group = models.CharField(max_length=32)
    zh = models.CharField(max_length=128)
    ja = models.CharField(max_length=128)
    en = models.CharField(max_length=128)
    status = models.CharField(max_length=32, default='translating')
    translated = models.BooleanField(default=False)


class Basic(models.Model):
    key = models.CharField(max_length=128, primary_key=True)
    value = models.CharField(max_length=128)
