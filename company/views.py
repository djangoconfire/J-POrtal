from django.shortcuts import render_to_response,render,get_object_or_404
from django.template import RequestContext
from django.http import HttpResponse , HttpResponseRedirect,JsonResponse,HttpResponseBadRequest
from django.contrib.auth.decorators import login_required 
from django.core.urlresolvers import reverse
from django.template.context_processors import csrf
from django.contrib.auth import authenticate,login,logout
from company.models import Company
from jobs.models import  JobListing,JobApplications,ShortlistedCandidates,MailToShortlisted
from user_profile.models import UserProfile
from django.db.models import Q
from django.contrib.auth.models import User
from forms import CompanyProfileForm,FinalShortlistedCandidateForm
from django.core.urlresolvers import reverse
from jobs import forms as job_form
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.core.mail import send_mail,EmailMessage
from django.template.loader import get_template
from jobseeker.models import JobSeeker
from django.contrib import messages
import StringIO
import xlwt
import xlrd
import json
import markdown
from django.conf import settings
from .utils import queryset_to_workbook
from jobs import forms as interview
from jobs.models import MailToCompany
from django.forms import modelformset_factory
#from forms import InterviewDetailForm


@login_required
def CreateCompanyProfile(request):
    data_dict={}
    if request.method=="POST":
        form=CompanyProfileForm(request.POST,request.FILES)
        if form.is_valid():
            post_data = request.POST
            file_data = request.FILES
            company_name = post_data.get('company_name', "")
            slug = post_data.get('slug', "")
            email = post_data.get('email', "")
            description = post_data.get('description', "")
            company_website = post_data.get('company_website', "")
            contact_no= post_data.get('contact_no', "")
            company_logo = file_data.get('company_logo', None)

            # validate company form
            error = validate_company_form(company_name,slug,company_website,description,email,contact_no,company_logo)
            if error is None:
                new_company=Company()
                new_company.company_name=company_name
                new_company.company_website=company_website
                new_company.description=description
                new_company.contact_no=contact_no
                new_company.slug=slug
                new_company.email=email
                new_company.company_name=company_name
                if company_logo is not None:
                    new_company.company_logo= company_logo
                new_company.save()
                ###slug=new_company.slug
                return HttpResponseRedirect(new_company.get_absolute_url())
            else:
                data_dict['error'] = error
                    
    else:
        form=CompanyProfileForm()   
    data_dict['form']=form         
    return render_to_response('company/create_company_profile.html',data_dict,context_instance=RequestContext(request))


@login_required
def ViewFullDetail(request,slug):
  instance=get_object_or_404(Company,slug=slug)
  return render_to_response('company/company_profile.html',{'instance':instance},context_instance=RequestContext(request))
    

@login_required
def UpdateCompanyProfile(request,slug):
  if request.method=="GET":
    instance=get_object_or_404(Company,slug=slug)
    form=CompanyProfileForm(instance=instance)
  if request.method=="POST":
    instance=get_object_or_404(Company,slug=slug)
    form=CompanyProfileForm(request.POST, request.FILES,instance=instance)
    if form.is_valid():
      instance=form.save(commit=False)
      instance.save()
      return HttpResponseRedirect(instance.get_absolute_url())

  context={
     'form':form,
     'instance':instance
          }  
  return render_to_response('company/company_update_profile.html',context,context_instance=RequestContext(request))



@login_required
def PostedJobByCompany(request,company_slug):
    company=get_object_or_404(Company,slug=company_slug)
    job_list=JobListing.objects.filter(company=company)
    return render_to_response('company/posted_job_by_company.html',{'company':company,'job_list':job_list},context_instance=RequestContext(request))
    



@csrf_exempt
def search(request):
    print '\n\n\n'
    print 'inside searching'
    print '\n\n\n'
    if request.method=='POST':
        search_text=request.POST['search_text']
    else:
        search_text=''

    companies=Company.objects.filter(company_name__icontains=search_text)
    return render(request,'company/ajax_company_search.html',{'companies':companies})        
    # try:
    #     query=request.GET.get('query','')
    # except Exception as e:
    #     return None
    # if query:
    #     companies=Company.objects.filter(Q(company_name__icontains=query)).distinct()
    #     count=len(companies)
    #     return render(request,'company/search.html',{'companies':companies,'query':query,'count':count})
    # else:
    #     return HttpResponse('No result found')            



    


def JobDetail(request,company_slug,job_slug):
    job=get_object_or_404(JobListing,slug=job_slug)
    form=job_form.JobCreatingForm(instance=job)
    ##job=get_object_or_404(slug=job_slug)
    return render(request,'company/job_detail.html',{'job':job,'form':form})

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
                if current_dict['name'] == 'description':
                    description = current_dict['value'].split(',')
                    print len(description)
                    html = 'Nothing to display :('
                    if len(description) > 0:
                        html = markdown.markdown(description[0], safe_mode='escape')
                    return HttpResponse(html)
                continue

    except Exception, e:
        return HttpResponseBadRequest()




@csrf_exempt
def CandidateSelection(request):
    if request.method=='POST':
        id = request.POST.get('id',0)
        print '\n\n\n'
        print id
        print '\n\n\n'
    try:
        application=JobApplications.objects.get(id=id)
        print '\n\n\n'
        print application.jobseeker.name
        print '\n\n\n'
    except Exception as e:
        ##message="Job Application does not exit"
        return JsonResponse({'success':'False','exception': e})
       
    application.action_by_team_leader = 'shortlisted'
    application.is_shortlisted=True
    application.is_rejected=False
    
    try:
        application.save()
        return JsonResponse({'success':'True'})
    except Exception as e:
        return JsonResponse({'success':'False','exception':e})
    return JsonResponse({'success':'False'})


@csrf_exempt
def CandidateRejection(request):
    if request.method=='POST':
        id = request.POST.get('id',0)
        print '\n\n\n'
        print id
        print '\n\n\n'
    try:
        application=JobApplications.objects.get(id=id)
        print '\n\n\n'
        print application.jobseeker.name
        print '\n\n\n'
    except Exception as e:
        ##message="Job Application does not exit"
        return JsonResponse({'success':'False','exception': e})
    
    application.action_by_team_leader = 'rejected'
    application.is_rejected=True
    application.is_shortlisted=False
            

    
    try:
        application.save()
        return JsonResponse({'success':'True'})
    except Exception as e:
        return JsonResponse({'success':'False','exception':e})
    return JsonResponse({'success':'False'})


def SendingMailToCompany(request,company_slug,job_slug):
    company=get_object_or_404(Company,slug=company_slug)
    job=get_object_or_404(JobListing,slug=job_slug)
    applications=JobApplications.objects.filter(job=job,action_by_team_leader="shortlisted")
    from_email=settings.EMAIL_HOST_USER
    to='ritu31195@gmail.com'
    site_name="AnalyticsVidhya"
    domain=request.META['HTTP_HOST']
    subject_template_name='company/mail_to_company.txt'
    email_template_name='company/shortlisted_form.html'
    subject_content=get_template(subject_template_name)
    email_content=get_template(email_template_name)
    context = RequestContext(request, locals())
    sub_content=subject_content.render(context)
    mail_content=email_content.render(context)
    html_message=mail_content
    application_id_list=[application.jobseeker.id for application in applications if not application.mail_to_company]
    jobseeker_queryset=JobSeeker.objects.filter(id__in=application_id_list)


    

    queryset = jobseeker_queryset
    columns = (
        'id',
        'name',
        'work_exp',
        'ug_course',
        'ug_institute_name',
        'pg_course',
        'pg_institute_name',
        'ctc',
        'current_employer',
        'current_designation',
        'current_location'
        )
    workbook = queryset_to_workbook(queryset, columns)

    response = HttpResponse(content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename="shortlisted_candidate.xls'
    workbook.save(response)
    ##return response
           

    message=EmailMessage(subject='ritu',
              body=html_message,
              from_email=from_email,
              to=[to]
              )

    message.attach('shortlisted_candidate.xls',response.getvalue(),"application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    message.send()

    for application in applications:
        application.mail_to_company=True
        application.save()

        

    return HttpResponse('mail successfully sent')


def FinalShortlistedCandidates(request,company_slug,job_slug):
     job=get_object_or_404(JobListing,slug=job_slug)
     company=get_object_or_404(Company,slug=company_slug)
     print company.slug,company
     applications=job.jobapplications_set.filter(job=job,action_by_team_leader="shortlisted")
     form_list=[]
     email_list=[]

     interview_form=interview.InterviewDetailForm()
     ###ShortlistedCandidateFormset=modelformset_factory(JobSeeker,extra=0,form=FinalShortlistedCandidateForm)

    
     return render(request,'company/company_shortlisted_candidate.html',{'company':company,'interview_form':interview_form,'job':job,'applications':applications})

       

@csrf_exempt
def SeeMore(request):
    if request.method=='POST':
        id = request.POST.get('id',0)
        print '\n\n\n'
        print id
        print '\n\n\n'

    try:
        application=JobApplications.objects.get(id=id)
        print '\n\n\n'
        print application.jobseeker.name
        print '\n\n\n'
    except Exception as e:
        ##message="Job Application does not exit"
        return JsonResponse({'success':'False','exception': str(e)})




    json_dict={}
    json_dict['serial_number']=application.jobseeker.serial_number
    json_dict['current_employer']=application.jobseeker.current_employer
    json_dict['jobseeker_name']=application.jobseeker.name
    if application.jobseeker.current_designation != None:         
        json_dict['current_designation']=application.jobseeker.current_designation.position
    else:
        json_dict['current_designation']="Not specified"    
    json_dict['ctc']=application.jobseeker.ctc
    # relavant_skill=[]
    # for skill in application.jobseeker.skills.all():
    #     relavant_skill.append(skill)

    # json_dict['relavant_skill']=relavant_skill
    json_dict['success']='True'
            
    return JsonResponse(json_dict) 


from dal import autocomplete



class CompanyAutocomplete(autocomplete.Select2QuerySetView):
    print 'inside company autocompletion'
    def get_queryset(self):
        # Don't forget to filter out results depending on the visitor !

        qs = Company.objects.all()

        if self.q:
            qs = qs.filter(company_name__istartswith=self.q)

        return qs

@csrf_exempt
def ShortlistedCandidates(request):
    print 'inside company selection'

    if request.method == 'POST':
        application_ids=request.POST.getlist('application_ids[]')
        print application_ids
        for application_id in application_ids:
            
            application=JobApplications.objects.get(id=application_id)
            print application.jobseeker.name,application.job
            print '@@@@@@@@@@@@@@@@@@@@@'

            job_title=application.job.job_title
            company=application.job.company.company_name
            job_location=application.job.job_location
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
            mail_content=email_content.render(context)


            send_mail('ritu','raj',
                      from_email,
                      [to],
                      fail_silently=False,
                      html_message=mail_content)
            print '\n\n\n\n\n'

            print application.jobseeker.name , application.job.job_title
            print '@@@@@@@@@@@@@@@@@@@@@@@@@@@@@'

            application.mail_sent_to_shortlisted=True
            application.save()

        return JsonResponse({'success':'True','application_ids':application_ids})    
    else:
        return JsonResponse({'success':'False','exception':'Not a post request'})  


def CompanyShortlistedCandidates(request,company_slug,job_slug):
     job=get_object_or_404(JobListing,slug=job_slug)
     company=get_object_or_404(Company,slug=company_slug)
     print company.slug,company
     applications=job.jobapplications_set.filter(job=job,action_by_team_leader="shortlisted")
     form_list=[]
     email_list=[]

     interview_form=interview.InterviewDetailForm()
     ###ShortlistedCandidateFormset=modelformset_factory(JobSeeker,extra=0,form=FinalShortlistedCandidateForm)

    
     return render(request,'recruiter/company_shortlisted.html',{'company':company,'interview_form':interview_form,'job':job,'applications':applications})



def validate_company_form(company_name,slug,company_website,description,email,contact_no,company_logo):
    if len(company_name) == 0:
        return "Company name is required"    
    if len(email) == 0:
        return "Email is required"
    if "@" not in email:
        return "Email is missing the '@' symbol"
    if len(company_website) == 0:
        return "Enter website name"
    if company_logo is not None:
        if profile_picture._size > 2048*1024:
            return "Max image size allowed is 2 mb"
    return None        

 




