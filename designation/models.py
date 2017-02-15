from __future__ import unicode_literals

from django.db import models


class Designation(models.Model):
    position=models.CharField(max_length=100,null=True,blank=True)

    def __unicode__(self):
        return self.position
