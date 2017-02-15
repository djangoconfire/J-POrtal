from django.db import models
from django.contrib.auth.models import User
from location.models import City,CorrectedCity
from taggit_autosuggest.managers import TaggableManager
from django.core.urlresolvers import reverse
from django.db.models.signals import pre_save
from django.utils.text import slugify
from autoslug import AutoSlugField
from designation.models import Designation
from decimal import Decimal


class JobSeeker(models.Model):

    YEAR_CHOICE=[(str(year),str(year)) for year in reversed(range(1950,2050))]

    EXP_CHOICE=[((exp),(exp)) for exp in range(1,20)]

    RECRUITER_ACTION=(
        
        ('not_interested','Not Interested'),
        ('interested','Interested'),
         ('not_answered','Not Answered'),
        )

    TEAM_LEADER_ACTION = (
            ('rejected','Rejected'),
            ('shortlisted','Shortlisted'),
            ('waiting','Put on Hold'),
            )


   

    
    serial_number                 = models.CharField(max_length=20,null=True,blank=True)
    resume2                       = models.CharField(max_length=15,null=True,blank=True)
                                                       #Django custom user
    name                          = models.CharField( max_length = 60 ) 
    contact_number                = models.CharField(max_length = 100, blank = True, null = True)                                              #name of the user
    email                         = models.EmailField(blank = True, null = True)  
    work_exp                      = models.DecimalField(decimal_places=2,max_digits=6,null=True, blank=True,default=Decimal(0))
    analytics_in_exp              = models.DecimalField(decimal_places=2,max_digits=6,null=True, blank=True,default=Decimal(0))
    current_location              = models.ForeignKey(City,blank=True,null=True,related_name="+")
    corrected_location            = models.ForeignKey(CorrectedCity,blank=True,null=True) 
    nearest_city                  = models.CharField(max_length = 250, blank = True, null = True) 
    preferred_location            = models.CharField(max_length = 250, blank = True, null = True)                                                                 #do you want your professional info to be shared among others  ? 
    ctc                           = models.CharField(max_length=20,null=True,blank=True)
    current_employer              = models.CharField(max_length = 150, blank = True, null = True) 
    current_designation           = models.ForeignKey(Designation,null=True,blank=True)      
    skills                        = TaggableManager()   
    ug_course                     = models.TextField(blank = True, null = True) 
    ug_course2                    = models.TextField(blank = True, null = True)                                                                 
    ug_institute_name             = models.CharField(max_length=100,blank=True,null=True)  
    tier1                         = models.NullBooleanField(default=False)
    ug_passing_year               = models.CharField(max_length=100,choices=YEAR_CHOICE,blank = True, null = True)
    pg_course                     = models.CharField(max_length=100,blank = True, null = True) 
    correct_pg_course             = models.CharField(max_length=100,blank = True, null = True)
    pg_institute_name             = models.CharField(max_length=100,blank=True,null=True)
    pg_tier1                      = models.NullBooleanField(default=False)
    pg_passing_year               = models.CharField(max_length=10,choices=YEAR_CHOICE,blank = True, null = True)
    resume                        = models.FileField( upload_to = "resume", blank = True, null = True ,default="/media/resume/resume2.pdf")               #file field to store location of resume
    profile_photo                 = models.ImageField( upload_to = "profile_photos", default="/static/images/default_profile_picture.png",blank = True, null = True )       #file field to store profile photo                     #Discourse username of the user
    address                       = models.TextField(blank = True, null = True)
    slug                          = AutoSlugField( populate_from="name",unique=True)
   
    expected_ctc                  = models.DecimalField(max_digits=10,decimal_places=2,null=True,blank=True)
    profile_cover_pic             = models.FileField( upload_to = "profile_cover_pic" ,default="/static/images/default_cover_picture.png",blank = True, null = True)                                                                                           #were the rules served to you. Obsolete field
                                         #your highest qualification     
                                                       #is UG regular ?
                                                                                  #your PG college ?
    
    about_me                      = models.TextField(blank = True, null = True)
    
    
    mail_sent_to_preferred        = models.NullBooleanField(null=True,blank=True)
    ready_to_relocate             = models.NullBooleanField(null=True,blank=True)
    notice_period                 = models.IntegerField(null=True,blank=True)
    #mail_to_company               = models.NullBooleanField(null=True,blank=True)
    # is_shortlisted                = models.NullBooleanField(blank=True,null=True)
    # is_rejected                   = models.NullBooleanField(blank=True,null=True)
    #mail_sent_to_shortlisted      = models.NullBooleanField(blank=True,null=True)
    # action_by_recruiter           = models.CharField(max_length = 20, blank = True, null = True, choices = RECRUITER_ACTION)
    # action_by_team_leader         = models.CharField(max_length = 20, blank = True, null = True, choices = TEAM_LEADER_ACTION)




    def get_absolute_url(self):
        return reverse('jobseeker:profile',kwargs={ "slug": self.slug})

    def get_image_url(self):
        return self.profile_photo.url 

    def get_resume_url(self):
        return self.resume.url     


    def __unicode__(self):
        return self.name
     


# def create_slug(instance,new_slug=None):
#     slug=slugify(instance.name)
#     if new_slug is not None:
#         slug=new_slug
#     qs=JobSeeker.objects.filter(slug=slug).order_by("-id")
#     exist=qs.exists()
#     if exist:
#         new_slug="%s-%s" %(slug,qs.first().id)
#         return create_slug(instance,new_slug=new_slug)
#     return slug
    

# def pre_save_post_jobseeker(sender,instance,*args,**kwargs):
#     if not instance.slug:
#         instance.slug=create_slug(instance)


# pre_save.connect(pre_save_post_jobseeker,sender=JobSeeker)











    












 
