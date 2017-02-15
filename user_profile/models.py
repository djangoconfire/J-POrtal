from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User 
from taggit_autosuggest.managers import TaggableManager
from location.models import City
import tinymce.models as tinymce_models


class UserProfile( models.Model ):
    
    USER_TYPE_CHOICES = (
            ('team_leader', "Team Leader"),
            ('recruiter',"Recruiter"),
            )
    user                          = models.OneToOneField( User)                                      #email address of the user
    user_type                     = models.CharField( max_length = 11, choices = USER_TYPE_CHOICES )# default =  user. other options are admin
    
#will work out on streak in the second version.    
    def __str__( self ):
        return str( self.user.username)


    class Meta :
        ordering = ['user']



class EmailMe(models.Model):
    to      = models.EmailField()
    subject = models.CharField(max_length=200)
    content = tinymce_models.HTMLField()

    def __unicode__(self):
        return self.to




   

