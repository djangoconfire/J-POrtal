from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.contrib.auth import  login, logout
from django.core.urlresolvers import reverse
from django.core.mail import send_mail
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import EmailMessage
from django.contrib.auth import authenticate

from company.models import Company
from user_profile.models import UserProfile 

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404



def home(request):
    return render_to_response('home.html',{},context_instance=RequestContext(request))



def user_login(request):
   
    context = RequestContext(request)
    if request.user.is_authenticated():
        #check if a user is authenticate
        try : 
            #try if userprofile exists
            user = UserProfile.objects.get(user = request.user)
        except UserProfile.DoesNotExist: 
            #if userprofile doesnot exist, redirect to all contests page
            return HttpResponseRedirect("/")
    if request.method == "GET":
        #if next is there in request.GET, send next in request data
        if 'next' in request.GET :   
            next_page = request.GET['next']
        else:
            next_page = ""
        return render_to_response('login.html', {"next":next_page}, context_instance = RequestContext(request))
        
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            user=UserProfile.objects.get(user=user)
            if user.user_type == 'team_leader':
                return HttpResponseRedirect('/' + 'user/' + request.POST.get('username',''))
            if user.user_type== 'recruiter':
                return HttpResponseRedirect('/' + 'user/' + request.POST.get('username',''))
                    
        else:
          return render_to_response("login.html",{"next":request.POST['next'], "error":"Invalid username or password. We treat username and email ids differently."}, context_instance = RequestContext(request)) #HttpResponseRedirect("/accounts/login/?next=/")  
        
@login_required
def user_logout(request):
    try :
        logout(request)
        return HttpResponseRedirect('/')
    except : 
        return HttpResponseRedirect("/")

