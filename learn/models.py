# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Person(models.Model):
    name = models.CharField(max_length=30)
    age = models.IntegerField()

class Blog(models.Model):
    name=models.CharField(max_length=100)
    tagline=models.TextField()

    def __unicode__(self):
        return self.name

class Author(models.Model):
    name=models.CharField(max_length=50)
    email=models.EmailField()

    def __unicode__(self):
        return self.name

