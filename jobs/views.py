
from django.shortcuts import render,render_to_response,get_object_or_404
from jobs.models import *
from user_profile.models import UserProfile
from django.contrib.auth.models import User 
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse , HttpResponseRedirect,JsonResponse
from django.template import RequestContext
from company.models import Company
from forms import JobCreatingForm
import json
import markdown
from taggit.models import Tag
from forms import InterviewDetailForm
from django.core.urlresolvers import reverse
from django.views.decorators.csrf import csrf_exempt


@login_required
def PostingNewJob(request):
    if request.method=="POST":
        form=JobCreatingForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/user/' + request.user.username)
    else:
        form=JobCreatingForm()
    return render_to_response('company/posting_new_job.html',{'form':form},context_instance=RequestContext(request))
 

'''
@login_required
def PostingNewJob(request):
    if request.method=="POST":
        form_data=request.POST.get('formData','')
        fojobrm_data_list=json.loads(form_data)
        length=len(form_data_list)

        for i in range(length):
            current_dict=form_data_list[i]

            if current_dict['name']=='job_title':
                new_job.job_title=current_dict['value']
                continue

            if current_dict['name']=='job_type':
                new_job.job_type=current_dict['value']
                continue 
                
            if current_dict['name']=='job_desc':
                new_job.job_desc=current_dict['value']
                continue
                
            if current_dict['name']=='job_min_exp':
                new_job.job_min_exp=current_dict['value']
                continue
                
            if current_dict['name']=='job_max_exp':
                new_job.job_max_exp=current_dict['value']
                continue
                

            if current_dict['name']=='job_min_ctc':
                new_job.job_min_ctc=current_dict['value']
                continue


            if current_dict['name']=='job_max_ctc':
                new_job.job_max_ctc=current_dict['value']
                continue  
                

            if current_dict['name']=='job_location':
                new_job.job_location=current_dict['value']
                try:
                    new_job.save()
                except Exception as e:
                    return JsonResponse({'success':'False','exception':str(e)})   
                continue
            
            if current_dict['name']=='as_values_id_tags__tagautosuggest':
                list_of_tags=current_dict['value'].split(',')
                for tag in list_of_tags:
                    if tag!='' and tag!=None:
                        tagobject=Tag.objects.get(name=tag)
                        new_job.job_skills.add(tagobject)
                continue                                     
            
        try:
            new_job.save()
        except Exception as e:
            return JsonResponse({'success':'False','exception':str(e)})
    else:
        form=JobCreatingForm()
    return render_to_response('company/posting_new_job.html',{'form':form},context_instance=RequestContext(request))
               
 '''          

def FinalSubmission(request):
    job_list=JobListing.objects.all().order_by('last_updated_date')
    return render_to_response('jobs/final_posted_job.html',{'job_list':job_list})

@login_required
def JobSeekerDashboard(request):
    if request.user.is_authenticated():
        try:
            user_profile=UserProfile.objects.get(user=request.user)
        except UserProfile.DoesNotExist:
            message="UserProfile does not exist"
            return render_to_response('500.html',{'error':message},context_instance=RequestContext(request))

    return render_to_response('jobs/job_seeker_dashboard.html',{},context_instance=RequestContext(request))


@login_required
#@ajax_required
@csrf_exempt
def preview(request):
    print 'inside preview'
    try:
        if request.method == 'POST':
            form_data=request.POST.get('form_data')
            print form_data
            form_data_list=json.loads(form_data)
            for i in range(len(form_data_list)):
                current_dict=form_data_list[i]
                print current_dict
                if current_dict['name'] == 'job_desc':
                    description = current_dict['value'].split(',')
                    print len(description)
                    html = 'Nothing to display :('
                    if len(description) > 0:
                        html = markdown.markdown(description[0], safe_mode='escape')
                    return HttpResponse(html)
                continue

    except Exception, e:
        return HttpResponseBadRequest()



@login_required
def EditJob(request,slug):
    if request.method=="GET":
        instance=get_object_or_404(JobListing,slug=slug)
        form=JobCreatingForm(instance=instance)
    if request.method=="POST":
        instance=get_object_or_404(JobListing,slug=slug)
        form=JobCreatingForm(request.POST, instance=instance)
        if form.is_valid():
            instance=form.save(commit=False)
            temp_tags=instance.job_skills.all()
            instance.job_skills.clear()
            ##instance.save()
            skill_data=request.POST.get('job_skills','')
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
                        instance.job_skills.add(skill_tag)
                    except Exception as e:
                        print e
                    
            instance.save()        
            return HttpResponseRedirect(instance.get_absolute_url())


    context={
     'form':form,
     'instance':instance
          }  
    return render_to_response('company/edit_job_form.html',context,context_instance=RequestContext(request))



# def JobDescription(request,job_slug):
#     job=get_object_or_404(JobListing,slug=job_slug)
#     return render(request,'jobseeker/job_description.html',{'job':job})



def Apply_to_job(request,jobseeker_slug,job_slug):

    job=get_object_or_404(JobListing,slug=job_slug)
    try:
        jobapplications = JobApplications.objects.get(job=job)
        if jobapplications.exists():
            for jobapplication in jobapplications:   
                context = {'job':job,'applied':True}
                return render(request,'jobseeker/job_description.html',context)
        else:
            return render(request,'500.html',{'error':'Job Application does not exist'})
    except Exception as e:
        context = {'job':job,'applied':False}
        return render(request,'jobseeker/job_description.html',context)

def SuccessfullyApplyForJob(request,jobseeker_slug,job_slug):
    try:
        jobseeker=get_object_or_404(JobSeeker,slug=jobseeker_slug)
        job = JobListing.objects.get(slug=job_slug)
    except Exception as e:
        return render_to_response("500.html", {"error" : e},
                context_instance = RequestContext(request))

    job.job_no_of_applications=job.job_no_of_applications + 1
    job.save()      
    newapplication = JobApplications()
    newapplication.jobseeker = jobseeker
    #newapplication.action="applied"
    newapplication.job = job 
    newapplication.save()
    context = {'jobseeker':jobseeker,'job':job}

    return render(request,'jobseeker/successfully_apply.html',context)



def Interview(request,company_slug,job_slug):
    print 'interview going on'
    #jobseeker=get_object_or_404(JobSeeker,slug=jobseeker_slug)
    company=get_object_or_404(Company,slug=company_slug)
    job=get_object_or_404(JobListing,slug=job_slug)
    if request.method=="POST":
        print '####'
        print 'enter in post method'
        form=InterviewDetailForm(request.POST)
        print '\n\n\n'
        print form
        if form.is_valid():
            print '\n\n\n'
            print 'enter in form'
            print '\n\n\n'
            interview_form=form.save(commit=False)
            #interview_form.jobseeker=JobSeeker
            interview_form.company=company
            interview_form.job=job
            interview_form.save()
            return HttpResponse('Record saved Successfully')
    else:
        form=InterviewDetailForm()
    return render(request,'company/interview.html',{'form':form,'job':job})        






    



        



    







