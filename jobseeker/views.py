from django.shortcuts import render,render_to_response,get_object_or_404
from django.template import RequestContext
from forms import JobSeekerMatchingProfileForm,JobSeekerProfileForm
from user_profile import forms as user_profile_forms

from django.http import HttpResponseRedirect,HttpResponse, JsonResponse
from user_profile.models import UserProfile
from django.contrib import messages 
from django.contrib.auth.decorators import login_required
from jobseeker.models import JobSeeker
from taggit.models import Tag
from django.views.decorators.csrf import csrf_exempt
import json
import traceback
from django.contrib import messages
from django.db.models import Q
from jobs.models import JobListing,JobApplications,MailToShortlisted
from django.conf import settings
from django.template.loader import get_template
from django.core.mail import send_mail,EmailMessage
from django.core.urlresolvers import reverse
from company.models import Company
from datetime import datetime
# from forms import PreferredCandidateForm,InterestedPreferredCandidateForm
from forms import InterestedPreferredCandidateForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.forms import modelformset_factory
from operator import and_
# from forms import SelectionForm
import re
from decimal import Decimal

## utility functions...


def intersect_list(a,b):
    return list(set(a) & set(b))

def union_list(a,b):
    return list(set(a) | set(b))

            

#form tables or other html.
def removenewline(value):
    values = str(value).split('\n')
    values = [value.replace('\r','') for value in values]
    new_value = ''.join(values)
    return unicode(str(new_value))    
    

def CreateJobSeekerProfile(request):
    if request.method=="POST":
        form=JobSeekerProfileForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/')
    else:
        form=JobSeekerProfileForm()
    return render_to_response('jobseeker/create_jobseeker_profile.html',{'form':form},context_instance = RequestContext(request))            

def JobSeekerProfile(request,slug):
    profile=get_object_or_404(JobSeeker,slug=slug)
    #job=get_object_or_404(JobListing,slug=job_slug)
    form = user_profile_forms.EmailMeForm()
    if request.method=="GET":
        instance=get_object_or_404(JobSeeker,slug=slug)
        update_profile_form=JobSeekerProfileForm(instance=instance)
    return render(request,'jobseeker/jobseeker_profile.html',{'form':form,'update_profile_form':update_profile_form,'profile':profile})



@login_required
def MatchingProfile(request):
    if request.user.is_authenticated():
        user=UserProfile.objects.get(user=request.user)
        form=JobSeekerMatchingProfileForm()
        return render_to_response('jobseeker/jobseeker_matching_profile.html',{'form':form},context_instance=RequestContext(request))
        


@csrf_exempt
@login_required
def SearchingMatchingProfile(request):
    form_data=request.POST.get('form_data','')
    form_data=json.loads(form_data)


    list_of_tags = ''
    jobseeker_list=JobSeeker.objects.all()
    query_list = [jobseeker for jobseeker in jobseeker_list] 

    for i in range(len(form_data)):
        current_dict = form_data[i]
        print current_dict


        if current_dict['name'] == 'job_min_exp':
            list_of_min_exp=current_dict['value'].split(',')
            for k in range(len(list_of_min_exp)):
                exp_id=list_of_min_exp[k]
                if exp_id != '' and exp_id != None:
                    try:
                        jobseekers = JobSeeker.objects.filter(work_exp__gte=int(exp_id))
                    except Exception as e:
                        print e
                        traceback.print_exc()
                    query_list=intersect_list(query_list,list(jobseekers)) 

        

        if current_dict['name'] == 'job_max_exp':
            list_of_max_exp=current_dict['value'].split(',')
            for k in range(len(list_of_max_exp)):
                exp_id=list_of_max_exp[k]
                if exp_id != '' and exp_id != None:
                    try:
                        jobseekers = JobSeeker.objects.filter(work_exp__lte=int(exp_id))
                    except Exception as e:
                        print e
                        traceback.print_exc()
                    query_list=intersect_list(query_list,list(jobseekers)) 


        if current_dict['name'] == 'job_min_ctc':
            list_of_min_ctc=current_dict['value'].split(',')
            for k in range(len(list_of_min_ctc)):
                ctc_id=list_of_min_ctc[k]
                if ctc_id != '' and ctc_id != None:
                    try:
                        jobseekers = JobSeeker.objects.filter(ctc__gte=int(ctc_id))
                    except Exception as e:
                        print e
                        traceback.print_exc()
                    query_list=intersect_list(query_list,list(jobseekers)) 

        if current_dict['name'] == 'job_max_ctc':
            list_of_max_ctc=current_dict['value'].split(',')
            for k in range(len(list_of_max_ctc)):
                ctc_id=list_of_max_ctc[k]
                if ctc_id != '' and ctc_id != None:
                    try:
                        jobseekers = JobSeeker.objects.filter(ctc__lte=int(ctc_id))
                    except Exception as e:
                        print e
                        traceback.print_exc()
                    query_list=intersect_list(query_list,list(jobseekers)) 
            

        if current_dict['name'] == 'job_location':
            list_of_location=current_dict['value'].split(',')
            for k in range(len(list_of_location)):
                location_id=list_of_location[k]
                print location_id
                if location_id != '' and location_id != None:
                    try:
                        jobseekers = JobSeeker.objects.filter(current_location=int(location_id))    

                    except Exception as e:
                        print e
                        traceback.print_exc()
                    query_list=intersect_list(query_list,list(jobseekers)) 
          
                     
    
        if current_dict['name'] == 'job_title':
            list_of_designation=current_dict['value'].split(',')
            for k in range(len(list_of_designation)):
                designation_id=list_of_designation[k]
                if designation_id != '' and designation_id != None:
                    try:
                        jobseekers = JobSeeker.objects.filter(current_designation=int(designation_id))
                        
                    except Exception as e:
                        print e
                        traceback.print_exc()
                    query_list=intersect_list(query_list,list(jobseekers)) 
               
             
        if current_dict['name'] == 'as_values_id_job_skills__tagautosuggest':
            list_of_tags = current_dict['value'].split(',')

            length = len(list_of_tags)
            print length
            print '^^^^^^^^^^^^^^^^^'

            for j in range(length):
                tagname = list_of_tags[j]
                if tagname!='' and tagname!=None:
                    try:
                        tag = Tag.objects.get(name=tagname)
                        jobseekers = intersect_list(query_list,[entry.content_object for entry in tag.taggit_taggeditem_items.all() if entry.content_type.name =='job seeker'])
                        print jobseekers
                
                    except Exception as e:
                        print "\n\n\n\n\nAn exception occurred while intersection of list\n\n\n\n" 
                        print e
                    query_list=intersect_list(query_list,list(jobseekers))    


                        
 
    list_of_matching_profiles = []
    for jobseeker in query_list:
        if jobseeker.current_location != None:
            location_name=jobseeker.current_location.city_name
        else:
            location_name = 'Not Specified'

        # if jobseeker.current_designation != None:
        #     designation_name=jobseeker.current_designation.position
        # else:
        #     designation_name = 'Not Specified'    
        skills_string = ''
        for skill in jobseeker.skills.all():
            skills_string += skill.name+","
        skills_string = skills_string[:-1]
        
        try:
            if jobseeker.resume:
                resume="Yes"
            else:
                resume="no"
        except:
            pass                

        # list_of_matching_profiles.append([jobseeker.get_image_url(),jobseeker.name,jobseeker.contact_number,jobseeker.email,
        #                                  jobseeker.ctc,skills_string,jobseeker.work_exp,location_name,designation_name,resume,jobseeker.slug,resume])

        list_of_matching_profiles.append([jobseeker.name,jobseeker.contact_number,jobseeker.email,
                                         jobseeker.ctc,skills_string,jobseeker.work_exp,location_name,resume,jobseeker.slug])
    print list_of_matching_profiles    
    return JsonResponse(list_of_matching_profiles,safe=False)


def UpdateProfile(request,slug):
    if request.method=="GET":
        instance=get_object_or_404(JobSeeker,slug=slug)
        form=JobSeekerProfileForm(instance=instance)
    if request.method=="POST":
        instance=get_object_or_404(JobSeeker,slug=slug)
        if request.FILES:
            form=JobSeekerProfileForm(request.POST, request.FILES,instance=instance)
        else:
            form=JobSeekerProfileForm(request.POST,instance=instance)   
        if form.is_valid():
            instance=form.save(commit=False)
            instance.skills.clear()
            skill_data=request.POST.get('skills','')
            print "THe skill data is \n\n\n"
            print skill_data
            list_of_skills = skill_data.split(',')
            for skill in list_of_skills:
                if skill != '' and skill != None:
                    try:
                        skill_tag = Tag.objects.get(name=skill)
                    except:
                        pass
                        
                    instance.skills.add(skill_tag)
                    instance.save()
            return HttpResponseRedirect(instance.get_absolute_url())


    context={
     'form':form,
     'profile':instance
          }  
    return render_to_response('jobseeker/update_profile.html',context,context_instance=RequestContext(request))


def Resume(request,slug):
    jobseeker_obj=get_object_or_404(JobSeeker,slug=slug)
    return render(request,'jobseeker/resume.html',{'jobseeker_obj':jobseeker_obj})


# @csrf_exempt
# def PreferredCandidate(request,job_slug):
    
#     try:
#         job=get_object_or_404(JobListing,slug=job_slug)
#     except Exception as e:
#         return render_to_response("500.html", {"error" : e},context_instance = RequestContext(request))
    

#     skill_list=[]
    
#     for job_skill in job.job_skills.all():
#         skill=str(job_skill).replace(' ','')

#         skill_list.append(skill)
#         for s in skill_list:
#             s.lower() 
#     jobseekers=JobSeeker.objects.filter(Q(skills__name__in=skill_list) & Q(work_exp__range=[job.job_min_exp,job.job_max_exp]))
#     seekers = [jobseeker for jobseeker in jobseekers]  #Get the list of corresponding users
#     jobseeker_id_list = [jobseeker.id for jobseeker in jobseekers]
#     selection_form=SelectionForm()
    


    
    

#     paginator=Paginator(jobseekers,3)
#     page=request.GET.get('page')
    

#     try:
#         jobseekers=paginator.page(page)
#     except PageNotAnInteger:
#         ## if page not an integer deliver to first page
#         jobseekers=paginator.page(1)
#     except EmptyPage:
#         ## page is out of range
#         jobseekers=paginator.page(paginator.num_pages)

#     count=len(jobseekers)    


#     context = {'count':count,'selection_form':selection_form,'jobseekers':jobseekers,'seekers':seekers,'job':job,'jobseeker_id_list':jobseeker_id_list}    
#     return render(request,'jobseeker/preferred_candidate.html',context)



   
def InterestedCandidate(request,job_slug):
    try:
        job = JobListing.objects.get(slug=job_slug)
    except Exception as e:
        return render_to_response("500.html", {"error" : e},context_instance = RequestContext(request))
    
    applications = JobApplications.objects.filter(job=job,action_by_recruiter="interested").distinct()
    seekers = [application.jobseeker for application in applications]  #Get the list of corresponding users
    application_id_list = [application.id for application in applications]

    print application_id_list
    print '***********************'

    paginator=Paginator(applications,6)
    page=request.GET.get('page')
    

    try:
        applications=paginator.page(page)
    except PageNotAnInteger:
        ## if page not an integer deliver to first page
        applications=paginator.page(1)
    except EmptyPage:
        ## page is out of range
        applications=paginator.page(paginator.num_pages)
    context = {'applications':applications,'seekers':seekers,'job':job,'application_id_list':application_id_list} 

    return render(request,'jobseeker/interested_jobseeker.html',context)



def ShortlistedCandidate(request,company_slug,job_slug):
    job=get_object_or_404(JobListing,slug=job_slug)
    company=get_object_or_404(Company,slug=company_slug)
    try:
        applications=JobApplications.objects.filter(job=job,action_by_team_leader="shortlisted")

    except Exception as e:
        return render_to_response("500.html", {"error" : e},context_instance = RequestContext(request))

    paginator=Paginator(applications,10)
    page=request.GET.get('page')
    

    try:
        applications=paginator.page(page)
    except PageNotAnInteger:
        ## if page not an integer deliver to first page
        applications=paginator.page(1)
    except EmptyPage:
        ## page is out of range
        applications=paginator.page(paginator.num_pages)    
    
            
    return render(request,'jobseeker/shortlisted_candidate.html',{'applications':applications,'time':datetime.now(),'job':job,'company':company})

# def InterestedCandidate(request,company_slug,job_slug):
#     job=get_object_or_404(JobListing,slug=job_slug)
#     try:
#         applications=JobApplications.objects.filter(action_by_recruiter="interested")
#         interested_jobseeker=JobSeeker()
#         interested_jobseeker.is_shortlisted=True
#         shortlisted_jobseeker.save()
#     except Exception as e:
#         return render_to_response("500.html", {"error" : e},context_instance = RequestContext(request))
    





def SendEmail(request,jobseeker_slug,job_slug):
    jobseeker=get_object_or_404(JobSeeker,slug=jobseeker_slug)
    job=get_object_or_404(JobListing,slug=job_slug)
    seeker_email=jobseeker.email
    to=seeker_email
    name=jobseeker.name
    job_title=job.job_title
    min_exp=job.job_min_exp
    max_exp=job.job_max_exp
    company=job.company.company_name
    job_location=job.job_location
    site_name="AnalyticsVidhya"
    domain=request.META['HTTP_HOST']
    apply_now_url=domain + reverse('jobs:apply_job' , args=[jobseeker_slug,job_slug])


    from_email=settings.EMAIL_HOST_USER
    subject_template_name='company/email_form.txt'
    email_template_name='company/email_form.html'
    subject_content=get_template(subject_template_name)
    context = RequestContext(request, locals())

    email_content=get_template(email_template_name)
    sub_content=subject_content.render(context)
    mail_content=email_content.render(context)
    # # Email subject *must not* contain newlines
    # #email = loader.render_to_string(email_template_name, c)
    # message =   "<strong>Dear"
    # message +=  "    <span style='margin-left:20px;'>" + name + "</span>"
    # message +=  "</strong>"
    # message +=  "<br/>"
    # message +=  "<p style='color:green;text-decoration:underline;'>"
    # message +=      "Jobs Matching your proifle"
    # message +=  "</p>"
    # message +=  "<br/>"     
    # message +=  "<div class='container'>"
    # message +=      "<div class='row'>"
    # message +=          "<div class='col-sm-5'>" 
    # message +=               job_title + '&nbsp;' +  '(' + str(min_exp)  + '-' + str(max_exp) + '&nbsp;' + 'yrs' + ')'
                            
    # message +=          "</div>"
    # message +=      "</div>"
    # message +=  "</div> "

    send_mail('ritu','raj',
              from_email,
              [to],
              fail_silently=False,
              html_message=mail_content)

    

    return HttpResponse('You habe been successfully applied for job')

def MailToShortlistedCandidates(request,job_slug):
    job=get_object_or_404(JobListing,slug=job_slug)
    job_title=job.job_title
    company=job.company.company_name
    job_location=job.job_location
    site_name="AnalyticsVidhya"
    domain=request.META['HTTP_HOST']
    to='ritu31195@gmail.com'


    from_email=settings.EMAIL_HOST_USER
    #subject_template_name='company/email_form.txt'
    email_template_name='jobseeker/email_shortlisted.html'
    #subject_content=get_template(subject_template_name)
    context = RequestContext(request, locals())

    email_content=get_template(email_template_name)
    #sub_content=subject_content.render(context)
    mail_content=email_content.render_to_response(context)


    send_mail('ritu','raj',
              from_email,
              [to],
              fail_silently=False,
              html_message=mail_content)


    k
    
    message.success(request,"Mail has been Successfully sent")

    try:
        application,created=JobApplications.objects.get(job=job,jobseeker=jobseeker)
        application.mail_to_shortlisted=True
        application.save()
    except Exception as e:
        print e    

  

    return HttpResponseRedirect('/user/' + 'user.username' )


from django.db.models import Prefetch
from .utilities import getMatch
def PreferredCandidate(request,job_slug):
    job=get_object_or_404(JobListing,slug=job_slug)
    skill_list=[]
    
    for job_skill in job.job_skills.all():
        skill=str(job_skill).strip()

        skill_list.append(skill)
        # for s in skill_list:
        #     s.lower() 
    jobseekers=JobSeeker.objects.filter(
        Q(skills__name__in=skill_list)
        ).distinct().prefetch_related(
            Prefetch(
                'jobapplications_set',
                queryset=JobApplications.objects.filter(job=job),#.values_list('action_by_recruiter',),
                to_attr="jobapplicationslist"
                )
            
            )

    seekers = [jobseeker for jobseeker in jobseekers]  #Get the list of corresponding users
    
    recruiterActionMap = {}
    mailSentMap = {}
    for s in jobseekers:
        for a in s.jobapplicationslist:
            recruiterActionMap[s.id]=a.action_by_recruiter
            mailSentMap[s.id] = a.mail_sent

    count=len(jobseekers)
    jobseekerList = []
    for seeker in jobseekers:
        job_seeker_map = {}
        job_seeker_map['id'] = seeker.id
        job_seeker_map['name'] = seeker.name
        job_seeker_map['email'] = seeker.email
        job_seeker_map['contact_number'] = seeker.contact_number
        job_seeker_map['serial_number'] = seeker.serial_number
        job_seeker_map['url'] = seeker.get_absolute_url()
        if(seeker.id in recruiterActionMap):
            job_seeker_map['action_by_recruiter'] = recruiterActionMap[seeker.id]
        else:
            job_seeker_map['action_by_recruiter'] = None
        if(seeker.id in mailSentMap):
            job_seeker_map['mail_sent'] = mailSentMap[seeker.id]
        else:
            job_seeker_map['mail_sent'] = None
        jobseekerList.append(job_seeker_map)
        jobSeekerSkill = [str(x) for x in seeker.skills.all()]
        skillMatchCountMap = getMatch(skill_list,jobSeekerSkill)
        job_seeker_map['matchMap']=skillMatchCountMap

    paginator=Paginator(jobseekerList,5)
    page=request.GET.get('page')
    try:
        jobseekers=paginator.page(page)
    except PageNotAnInteger:
        ## if page not an integer deliver to first page
        jobseekers=paginator.page(1)
    except EmptyPage:
        ## page is out of range
        jobseekers=paginator.page(paginator.num_pages)  
    context = {'jobseekers':jobseekers,'count':count}   
    
    return render(request,'recruiter/preferred_candidate.html',context)

@csrf_exempt
def SelectingPreferredCandidate(request):
    print 'inside selection'
    if request.method=="POST":
        jobSlug = request.POST.get('jobSlug','')
        jobSeekerId = request.POST.get('jobSeekerId','')
        action_by_recruiter = request.POST.get('action_by_recruiter','')
        print(jobSlug,jobSeekerId,action_by_recruiter)
        job = None
        jobSeeker = None
        actions = ['interested','not_interested','not_answered']
        flag = True
        response = None
        if(action_by_recruiter not in actions):
            flag = False
            context = {
                'status': '400', 'reason': 'Wrong action'  
            }
            response = JsonResponse(context)
        try:
            job = JobListing.objects.get(slug = jobSlug)
            jobseeker = JobSeeker.objects.get(id = jobSeekerId)
            jobApplication,created = JobApplications.objects.get_or_create(job = job,jobseeker=jobseeker)

            jobApplication.action_by_recruiter = action_by_recruiter
            jobApplication.save()
        except:
            flag=False
        if(not flag):
            context = {
                "success":True,"message":"invalid job application"  
            }
            response = JsonResponse(context)
            response.status_code = 400
        else:
            context = {
                "success":True,"message":"candidate status changed"  
            }
            response = JsonResponse(context)
        return response

        ## make validator

    #     data_dict={}
    #     form_data = request.POST.get('form_data','')
    #     form_data_list = json.loads(form_data)
    #     slug = request.POST.get('job_slug','')
    #     job=get_object_or_404(JobListing,slug=slug)
    #     print '\n\n\n'
    #     print job.job_title
        

      
    #     length = len(form_data_list)
    #     print length

    #     for i in range(length):
    #         current_dictionary = form_data_list[i]

    #         if  re.search(r'form-\d+-id',current_dictionary['name']):
    #             list_of_form=current_dictionary['value'].split(',')
    #             for k in range(len(list_of_form)):
    #                 form_id=list_of_form[k]
    #                 print '\n\n\n'
    #                 print form_id
    #                 print '$$$$$$$$$$$$$$$$$$$$$'
    #                 if form_id != '' and form_id != None:
    #                     try:
    #                         jobseeker=JobSeeker.objects.get(id=form_id)
    #                         print jobseeker.name
    #                         print 'try block end'
    #                     except Exception as e:
    #                         return JsonResponse({'success':'False','exception':str(e)})
                           

    #         if current_dictionary['name'] == 'selection':
    #             print 'inside selection'
    #             print '^^^^^^^^^^^^^^'
    #             list_of_selection=current_dictionary['value'].split(',')
    #             for k in range(len(list_of_selection)):
    #                 selection_id=list_of_selection[k]

    #                 if selection_id != '' and selection_id != None:
    #                     try:
    #                         application=JobApplications.objects.create(action_by_recruiter=selection_id)
    #                         application.job=job
    #                         application.jobseeker=jobseeker
    #                     except Exception as e:
    #                         return JsonResponse({'success':'False','exception':str(e)})


    #     try:
    #         application.save()
    #     except Exception as e:
    #         return JsonResponse({'success':'False','exception':str(e)})
        
    # data_dict['success']='True'
    # data_dict['jobseeker_slug']=application.jobseeker.slug
    # data_dict['jobseeker_name']=application.jobseeker.name
    # data_dict['serial_number']=application.jobseeker.serial_number
    # data_dict['contact_number']=application.jobseeker.contact_number
    # data_dict['email']=application.jobseeker.email
    # data_dict['form_id']=form_id
    # data_dict['selection_id']=application.action_by_recruiter
    
    return JsonResponse({'hello':1})      
##@csrf_exempt
def EditInterestedCandidate(request,jobseeker_slug,job_slug):
    print 'inside edit intrested candidate selection'
    jobseeker=get_object_or_404(JobSeeker,slug=jobseeker_slug)
    print jobseeker.name
    print '@@@@@@@@@@@@@@@@@@@@@'
    if request.method=="POST":
        form=InterestedPreferredCandidateForm(request.POST, instance=jobseeker)
        if form.is_valid():
            instance=form.save(commit=False)
            temp_tags=instance.skills.all()
            instance.skills.clear()
            ##instance.save()
            skill_data=request.POST.get('skills','')
            print "THe skill data is \n\n\n"
            print skill_data
            list_of_skills = skill_data.strip().split(',')
            for skill in list_of_skills:
                
                if skill != '' and skill != None and len(skill)>0:
                    try:
                        print("skill ::: ", skill)
                        skill_tag = Tag.objects.get(name=skill)
                        ##tagList.append(skill_tag)
                        print(skill_tag.slug)
                        instance.skills.add(skill_tag)
                    except Exception as e:
                        print e
                    
            instance.save()       
            return HttpResponseRedirect('/jobseeker/'+job_slug+'/preferred_interested_candidate/')
    else:
        return HttpResponse('Interested Profile not updated')        

    context={
     'form':form,
     'jobseeker':jobseeker
          }  
    return render(request,'jobseeker/edit_interested_candidate.html',context)

@csrf_exempt
## ajax request
def EditInterestedCandidate2(request):
    ##print 'inside edit intrested candidate selection'
    if request.method== 'POST':
        json_dict={}
        application_id=request.POST.get('application_id','')
        application=JobApplications.objects.get(id=application_id)

        jobseeker=application.jobseeker
        
        form = InterestedPreferredCandidateForm(instance=jobseeker)
        form_as_table = removenewline(form.as_table())
        json_dict['success']='True'
        json_dict['form']=form_as_table
        json_dict['jobseeker_slug']=application.jobseeker.slug
        json_dict['job_slug']=application.job.slug
        return JsonResponse(json_dict)

    else:
        return JsonResponse({'success':'False','exception':"The ajax method is not post"})





def InterestedPreferredCandidate(request,job_slug):
    form_list=[]
    job=get_object_or_404(JobListing,slug=job_slug)

    applications=JobApplications.objects.filter(job=job,action_by_recruiter="interested")
    
    for application in applications:
         form=InterestedPreferredCandidateForm(instance=application.jobseeker)

   
    
    paginator=Paginator(applications,3)
    page=request.GET.get('page')
    

    try:
        jobseekers=paginator.page(page)
    except PageNotAnInteger:
        ## if page not an integer deliver to first page
        jobseekers=paginator.page(1)
    except EmptyPage:
        ## page is out of range
        jobseekers=paginator.page(paginator.num_pages)
    
    
        
    return render(request,'recruiter/interested_candidate.html',{'applications':applications,'form':form,'job':job,'jobseekers':jobseekers})
@csrf_exempt    
def SendingJobDetail(request):
    if request.method=="POST":
        job_slug=request.POST.get('jobSlug','')
        jobSeekerId=request.POST.get('jobSeekerId','')
        try:
            job=get_object_or_404(JobListing,slug=job_slug)
            print job
        except Exception as e:
            return JsonResponse({'success':'False','exception':str(e)})

        try:
            jobseeker=get_object_or_404(JobSeeker,id=jobSeekerId)
            print jobseeker.name
        except Exception as e:
            return JsonResponse({'success':'False','exception':str(e)})


            
        jobseeker_name=jobseeker.name
        job_title=job.job_title
        company=job.company.company_name
        job_location=job.job_location
        job_min_exp=job.job_min_exp
        job_max_exp=job.job_max_exp
        site_name="AnalyticsVidhya"
        domain=request.META['HTTP_HOST']
        # to=jobseeker.email
        to='ritu31195@gmail.com'


        from_email=settings.EMAIL_HOST_USER
        #subject_template_name='company/email_form.txt'
        email_template_name='jobseeker/sending_job_detail.html'
        #subject_content=get_template(subject_template_name)
        context = RequestContext(request, locals())

        email_content=get_template(email_template_name)
        #sub_content=subject_content.render(context)
        mail_content=email_content.render(context)


        send_mail('ritu','raj',
                  from_email,
                  [to],
                  fail_silently=False,
                  html_message=mail_content)

        try:
            jobApplication,created = JobApplications.objects.get_or_create(job = job,jobseeker=jobseeker)

            jobApplication.mail_sent = True
            jobApplication.save()
            print jobApplication.jobseeker.name,jobApplication.mail_sent
            print '###################'
        except Exception as e:
            return JsonResponse({'success':'False','exception':str(e)})

      

        return JsonResponse({'success':'True','message':'Mail has been successfully sent'} ) 
    else:
        return JsonResponse({'success':'False','message':'Not a post request'})      
                 

@csrf_exempt    
def SendingJobDetail(request):
    if request.method=="POST":
        job_slug=request.POST.get('jobSlug','')
        jobSeekerId=request.POST.get('jobSeekerId','')
        try:
            job=get_object_or_404(JobListing,slug=job_slug)
            print job
        except Exception as e:
            return JsonResponse({'success':'False','exception':str(e)})

        try:
            jobseeker=get_object_or_404(JobSeeker,id=jobSeekerId)
            print jobseeker.name
        except Exception as e:
            return JsonResponse({'success':'False','exception':str(e)})


            
        jobseeker_name=jobseeker.name
        job_title=job.job_title
        company=job.company.company_name
        job_location=job.job_location
        job_min_exp=job.job_min_exp
        job_max_exp=job.job_max_exp
        site_name="AnalyticsVidhya"
        domain=request.META['HTTP_HOST']
        # to=jobseeker.email
        to='ritu31195@gmail.com'


        from_email=settings.EMAIL_HOST_USER
        #subject_template_name='company/email_form.txt'
        email_template_name='jobseeker/sending_job_detail.html'
        #subject_content=get_template(subject_template_name)
        context = RequestContext(request, locals())

        email_content=get_template(email_template_name)
        #sub_content=subject_content.render(context)
        mail_content=email_content.render(context)


        send_mail('ritu','raj',
                  from_email,
                  [to],
                  fail_silently=False,
                  html_message=mail_content)

        try:
            jobApplication,created = JobApplications.objects.get_or_create(job = job,jobseeker=jobseeker)

            jobApplication.mail__to_preferred = True
            jobApplication.save()
            print jobApplication.jobseeker.name,jobApplication.mail_sent
            print '###################'
        except Exception as e:
            return JsonResponse({'success':'False','exception':str(e)})

      

        return JsonResponse({'success':'True','message':'Mail has been successfully sent'} ) 
    else:
        return JsonResponse({'success':'False','message':'Not a post request'})      
                 
