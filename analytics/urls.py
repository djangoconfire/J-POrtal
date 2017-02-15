"""analytics URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include,patterns
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings

#from user_profile import views as profile_views
from . import views
from django.views.static import serve
from ajax_select import urls as ajax_select_urls

admin.autodiscover()
urlpatterns = [
   
    url(r'^$','analytics.views.home',name='home_view'),
    url(r'^admin/', admin.site.urls),
    url(r'^accounts/login/', views.user_login, name='login'),
    url(r'^accounts/logout/', views.user_logout, name='logout'),
    url(r'^user/',include('user_profile.urls',namespace="user_profile",app_name="user_profile")),
    url(r'^jobs/',include('jobs.urls',namespace="jobs",app_name="jobs")),
    url(r'^jobseeker/',include('jobseeker.urls',namespace="jobseeker",app_name="jobseeker")),
    url(r'^company/',include('company.urls',namespace="company",app_name="company")),
    url(r'^taggit_suggest/', include('taggit_autosuggest.urls')),
    url(r'^recruiter/', include('recruiter.urls',namespace="recruiter")),

    url(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    url(r'^admin/lookups/', include(ajax_select_urls)),
    
    url(r'^tinymce/', include('tinymce.urls')),
    url('^markdown/', include( 'django_markdown.urls')),
    url(r'^api/jobs/',include('jobs.api.urls',namespace="api-jobs")),
    url(r'^ajax/add_designation/$','designation.views.AddingNewDesignation',name="new_designation"),
    url(r'^ajax/add_city/$','location.views.AddingNewCity',name="new_city"),




    
]


