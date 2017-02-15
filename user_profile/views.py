
from django.shortcuts import render,render_to_response,redirect,get_object_or_404
from django.template import RequestContext
from jobs.models import *
from company.models import *
from user_profile.models import *
from django.template.context_processors import csrf
from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponse , HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate
from user_profile.models import UserProfile
from user_profile.forms import SignUpForm,EmailMeForm
from django.contrib.auth.models import User
from django.contrib import messages
from jobseeker.models import *
from django.core.mail import send_mail
from django.conf import settings
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.template import loader
from django.template.loader import get_template
from company.forms import CompanySearchForm

import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def signup(request):
    choices=UserProfile.USER_TYPE_CHOICES
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if not form.is_valid():
            return render(request, 'signup.html', {'form': form})

        else: 
            user_type=form.cleaned_data.get('user_type')
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            djangouser = User(username=username)
            djangouser.set_password(password)
            djangouser.email = email 
            try:
                djangouser.save()
            except Exception as e:
                form = SignUpForm()
                return render(request,'signup.html',{'form':form})

            new_user=UserProfile()
            new_user.user_type=user_type

            
            user = authenticate(username=username, password=password)
            ## user has been added to the current session
            new_user.user = djangouser
            new_user.save()
                    
            login(request, user)

            if user_type=="team_leader":
                return render_to_response('profile/team_leader_profile2.html',{}, context_instance = RequestContext(request))
            if user_type=='recruiter':
                return render_to_response('recruiter/dashboard.html',{}, context_instance = RequestContext(request))


            ##return redirect('/')
    else:
        return render(request, 'signup.html', {'form': SignUpForm(),'choices':choices})


@login_required
def user_profile(request,username):
    if request.user.is_authenticated():
        try:
            user=UserProfile.objects.get(user=request.user)
            job_list=JobListing.objects.all().order_by('-last_updated_date')
            paginator=Paginator(job_list,3)
            page=request.GET.get('page')
            

            try:
                jobs=paginator.page(page)
            except PageNotAnInteger:
                ## if page not an integer deliver to first page
                jobs=paginator.page(1)
            except EmptyPage:
                ## page is out of range
                jobs=paginator.page(paginator.num_pages)        


            
        except UserProfile.DoesNotExist:
            message="UserProfile does not exist"
            return render_to_response('500.html',{'error':message},context_instance = RequestContext(request))

    company_search_form=CompanySearchForm()
    if user.user_type=='team_leader':
        return render_to_response('profile/team_leader_profile2.html',{'jobs':jobs,'company_search_form':company_search_form},context_instance = RequestContext(request)) 

    if user.user_type=='recruiter':
        return render_to_response('recruiter/dashboard.html',{'jobs':jobs},context_instance = RequestContext(request))
        
    return HttpResponse('something went wrong')    

@login_required
def SendEmail(request):
    #jobseeker_obj=get_object_or_404(JobSeeker,slug=slug)
    if request.method == 'POST':
        form=EmailMeForm(request.POST)
        if form.is_valid():
            to=form.cleaned_data.get('to')
            subject=form.cleaned_data.get('subject')
            content=form.cleaned_data.get('content')

            form.save()
            from_email=settings.EMAIL_HOST_USER
            jobseeker_obj=JobSeeker.objects.get(email=to)
            to=jobseeker_obj.email
            slug=jobseeker_obj.slug

            c = {
                'email': to,
                'name':jobseeker_obj.name,
                'slug':slug,
                'domain': 'analyticsvidhya.com', #or your domain
                'site_name': 'analyticsvidhya',
                'designation': jobseeker_obj.current_designation.position,
                'location':jobseeker_obj.current_location,
                }


            subject_template_name='company/email_form.txt'
            email_template_name='company/email_form.html'
            subject_content=get_template(subject_template_name)

            template_content=get_template(email_template_name)
            sub_content=subject_content.render(c)
            content=template_content.render(c)
            # Email subject *must not* contain newlines
           #email = loader.render_to_string(email_template_name, c)
            send_mail(sub_content, content, from_email, [to], fail_silently=False)
            
        
            
            #print "mail not sent"
                    
            return HttpResponse('Your Message has been submitted')
    else:
        form=EmailMeForm()
    return render(request,'company/email_me_form.html',{'form':form})            
    





