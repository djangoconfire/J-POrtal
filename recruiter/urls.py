from django.conf.urls import url,include

from views import *

urlpatterns=[
      
     url(r'^dashboard/$','recruiter.views.Dashboard',name="dashboard"),


    ]