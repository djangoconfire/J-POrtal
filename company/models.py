from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User 
from django.core.urlresolvers import reverse
from django.db.models.signals import pre_save
from django.utils.text import slugify
from user_profile.models import UserProfile
from jobseeker.models import JobSeeker
from tinymce import models as tinymce_models
import markdown


#from taggit.managers import TaggableManager


def get_image_path(instance,filename):
    return os.path.join('company_logo',str(instance.id),filename)
            


class Company(models.Model):
    #user=models.OneToOneField(UserProfile)
    company_name=models.CharField(unique=True,max_length=100)
    slug=models.SlugField(unique=True)
    company_website=models.URLField()
    description=models.TextField()
    company_logo=models.ImageField(upload_to='company_logo',blank=True,default="/static/images/company-logo.png")
    contact_no=models.CharField(max_length=100,blank=True,null=True)
    email=models.EmailField()
    estabished_year=models.IntegerField(null=True,blank=True)
    no_of_employes=models.IntegerField(null=True,blank=True)
    mail_sent_to_company=models.NullBooleanField(blank=True)


    def __unicode__(self):
        return self.company_name

    def get_absolute_url(self):
    	return reverse('company:full_detail',args=[self.slug])

    def get_content_as_markdown(self):
        return markdown.markdown(self.description, safe_mode='escape')    



def create_slug(instance,new_slug=None):
    slug=slugify(instance.company_name)
    if new_slug is not None:
        slug=new_slug
    qs=Company.objects.filter(slug=slug).order_by("-id")
    exist=qs.exists()
    if exist:
        new_slug="%s-%s" %(slug,qs.first().id)
        return create_slug(instance,new_slug=new_slug)
    return slug
    

def pre_save_post_company(sender,instance,*args,**kwargs):
    if not instance.slug:
        instance.slug=create_slug(instance)


pre_save.connect(pre_save_post_company,sender=Company)




# class InterviewDetail(models.Model):

#     INTERVIEW_CHOICES=(
#             ('face_to_face',"Face to Face"),
#             ('telephonic',"Telephonic"),
#         )
#     jobseeker=models.ForeignKey(JobSeeker)
#     company=models.ForeignKey(Company)
#     date_of_interview=models.DateField()
#     time_start=models.DateTimeField()
#     time_end=models.DateTimeField()
#     interview_choice=models.CharField(max_length=20,choices=INTERVIEW_CHOICES)

#     def __unicode__(self):
#         return self.interview_choice





      




            

   



    




