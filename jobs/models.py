from __future__ import unicode_literals

from django.db import models
from django.utils import timezone
#from autoslug import AutoSlugField
from django.core.exceptions import ValidationError
from user_profile.models import UserProfile 
from company.models import Company
from django.utils.translation import ugettext_lazy as _
from taggit_autosuggest.managers import TaggableManager
from location.models import City
from designation.models import Designation
from autoslug import AutoSlugField
from django.utils import timezone
from jobseeker.models import JobSeeker
from django.db.models import Q
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
import markdown
from taggit.models import Tag
#from skill.models import SkillsRequired


class JobListing(models.Model) : 
    
    JOB_TYPE_CHOICES = (
            ('fulltime','Full Time'),
            ('contract','Contract'),
            ('intern','Intern'),
            ('freelance','Freelance'),
            ('parttime','Part Time')
    )
    
    EXP_CHOICES=[(int(item),int(item)) for item in range(1,20)]

    JOB_CTC_CHOICE=[(item,item) for item in range(1,20)]




    company                      = models.ForeignKey(Company,null=True,help_text="<strong>Select Company from dropdown")
    job_title                    = models.ForeignKey(Designation,null=True,blank=True)
    slug                         = AutoSlugField( populate_from="job_title",unique=True)
    
     
    
    job_type                     = models.CharField(max_length = 10, blank  = True, null = True, 
                                   choices = JOB_TYPE_CHOICES, help_text = '<strong>Select Type of job </strong>')
    job_desc                     = models.TextField()
    job_min_ctc                  = models.IntegerField(choices=JOB_CTC_CHOICE,null = True)
    job_max_ctc                  = models.IntegerField(choices=JOB_CTC_CHOICE,null = True)
    job_min_exp                  = models.IntegerField(choices=EXP_CHOICES)
    job_max_exp                  = models.IntegerField(choices=EXP_CHOICES)
    job_location                 = models.ForeignKey(City,blank=True,null=True)
    #current_designation          = 
    job_skills                   = TaggableManager()
    #relavant_skill               = models.ForeignKey(SkillsRequired,blank=True,null=True)
    pub_date                     = models.DateTimeField(auto_now_add = True,blank=True,null=True)
    last_updated_date            = models.DateTimeField(auto_now=True,blank=True,null=True)
    job_no_of_applications       = models.IntegerField(default=0,blank=True)
    responsibility               = models.TextField(null=True,blank=True)
    qualification                = models.TextField(null=True,blank=True)



    ##interested_candidates=property(interested_candidate)

    def PreferredCandidates(self): 
        job=JobListing.objects.get(slug=self.slug)
        skill_list=[]
    
        for job_skill in job.job_skills.all():
            skill=str(job_skill).replace(' ','')

            skill_list.append(skill)
            for s in skill_list:
                s.lower()  
        jobseekers=JobSeeker.objects.filter(Q(skills__name__in=skill_list)).distinct()
        print jobseekers.count()
        print '$$$$$$$$$$$$$$$$$$$$$$$$$$$'
        return jobseekers.count()

    def interested_candidates_count(self):
        return self.jobapplications_set.filter(action_by_recruiter="interested").distinct().count()


    def shortlisted_candidates_count(self):
        return self.jobapplications_set.filter(action_by_team_leader="shortlisted").count() 

    def final_shortlisted_candidates_count(self):
        return self.jobapplications_set.filter(mail_sent_to_shortlisted=True).count() 

    def final_shortlisted_candidates(self):
        return self.shortlistedcandidates_set.all()    
        
    preferred_candidates=property(PreferredCandidates) 
    interested_candidates=property(interested_candidates_count)    
    shortlisted_candidates=property(shortlisted_candidates_count)    

    final_shortlisted_candidates=property(final_shortlisted_candidates_count)    
    final_shortlisted=property(final_shortlisted_candidates)

       

    def __str__(self):
        return "%s " %(self.job_title)

        
    class Meta : 
        ordering = ['-job_min_ctc']


    def get_absolute_url(self):
        return reverse('company:job_detail',kwargs={ "company_slug": self.company.slug, "job_slug": self.slug})


    def get_time_diff(self):
        return (timezone.now() - self.pub_date).seconds


    def get_content_as_markdown(self):
        return markdown.markdown(self.job_desc, safe_mode='escape')    
    



class JobApplications(models.Model) :
    
    
    SOURCE_OF_ACTION = (
            ('mail','E-Mail'),
            ('sms','SMS'),
     )

    TEAM_LEADER_ACTION = (
            ('rejected','Rejected'),
            ('shortlisted','Shortlisted'),
            ('waiting','Put on Hold'),
            )


    RECRUITER_ACTION=(
        
        ('not_interested','Not Interested'),
        ('interested','Interested'),
        ('not_answered','Not Answered'),
        )


    jobseeker               = models.ForeignKey(JobSeeker,null=True, blank=True)
    job                     = models.ForeignKey(JobListing,null=True, blank=True)
    mail_sent               = models.NullBooleanField(default = False)
    mail_sent_at            = models.DateTimeField(auto_now_add=True,blank = True, null = True)
    sms_sent_at             = models.DateTimeField(auto_now_add=True,blank = True,null = True)
    viewed_at               = models.DateTimeField(auto_now_add=True,blank = True,null = True)
    #action                  = models.CharField(max_length = 20, blank = True, null = True, choices = ACTION_CHOICES)
    source_of_action        = models.CharField(max_length = 20, blank = True, null = True, choices = SOURCE_OF_ACTION)
    time_of_action          = models.DateTimeField(auto_now_add=True,blank = True,null = True) # as soon as the user comes to  a particular listing, 
    action_by_team_leader   = models.CharField(max_length = 20, blank = True, null = True, choices = TEAM_LEADER_ACTION)
    action_by_recruiter     = models.CharField(max_length = 20, blank = True, null = True, choices = RECRUITER_ACTION)
    is_shortlisted          = models.NullBooleanField(blank=True,null=True)
    is_rejected             = models.NullBooleanField(blank=True,null=True)
    mail_to_company         = models.NullBooleanField(null=True,blank=True)
    mail_sent_to_shortlisted= models.NullBooleanField(blank=True,null=True)
    ##job_detail_sent_to_interested = models.NullBooleanField(blank=True,null=True)

    def get_team_leader_action(self) : 
        if not self.action_by_company : 
            return None 
        action_short_name = ['rejected','shortlisted','waiting']
        action_large_name = ['Rejected','Shortlisted','Put on Hold']
        return action_large_name[action_short_name.index(self.action_by_team_leader)]

    def return_source_of_action(self):
        if not self.source_of_action : 
            return None 
        sources_short_name = ['mail','sms']
        sources_full_name  = ['E-Mail','SMS']
        return sources_full_name[sources_short_name.index(self.source_of_action)]


    def get_edit_interested_candidate(self):
        return reverse('jobseeker:get_edit_interested_candidate',kwargs={ "jobseeker_slug": self.jobseeker.slug, "job_slug": self.slug})
    
    class Meta : 
        ordering = ['-mail_sent_at','-sms_sent_at','-time_of_action']   







class PreferredCandidate(models.Model):
    jobseeker=models.ForeignKey(JobSeeker)
    job=models.ForeignKey(JobListing)

class ShortlistedCandidates(models.Model):
    mail_sent=models.BooleanField()
    jobseeker=models.ForeignKey(JobSeeker)
    job=models.ForeignKey(JobListing)

    def __unicode__(self):
        return self.jobseeker.name

        



class InterviewDetail(models.Model):

    INTERVIEW_CHOICES=(
            ('face_to_face',"Face to Face"),
            ('telephonic',"Telephonic"),
        )
    #jobseeker=models.ForeignKey(JobSeeker)
    company=models.ForeignKey(Company)
    job=models.ForeignKey(JobListing)
    date_of_interview=models.DateField()
    time_start=models.DateTimeField()
    time_end=models.DateTimeField()
    interview_choice=models.CharField(max_length=20,choices=INTERVIEW_CHOICES)

    def __unicode__(self):
        return self.interview_choice






class MailToCompany(models.Model):
    mail_sent=models.BooleanField()
    company=models.ForeignKey(Company)
    jobseeker=models.ForeignKey(JobSeeker)

    def __unicode__(self):
        return 'Mail sent to company %s  ' % (self.company.company_name)


class MailToShortlisted(models.Model):
    jobseeker=models.ForeignKey(JobSeeker,related_name="job")
    job=models.ForeignKey(JobListing)
    mail_to_shortlisted=models.NullBooleanField()

    def __unicode__(self):
        return 'mail sent to %s shortlisted for %s ' %(self.jobseeker.name,self.job.job_title)


        



  




