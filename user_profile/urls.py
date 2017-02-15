from django.conf.urls import url,include

from views import *

urlpatterns=[
			
		

        url(r'^sign_up/$','user_profile.views.signup',name="signup"),      
        url(r'^send_mail/$','user_profile.views.SendEmail',name="sending_mail"),
        url(r'^(?P<username>.*)$','user_profile.views.user_profile',name="logged_in_user"),
        
        

    ]
