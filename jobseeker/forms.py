from django import forms
from models import JobSeeker
from jobs.models import JobListing
from django.forms import ModelForm


class JobSeekerProfileForm(forms.ModelForm):
   class Meta:
      model=JobSeeker
      exclude=['user','mail_sent']

      labels={
         'tags':'Skills'
      }



      widgets={
         'name':forms.TextInput(attrs={'class':'form-control','placeholder':'Enter your name'}),
         'email':forms.TextInput(attrs={'class':'form-control','placeholder':'example@gmail.com'}),
         'current_designation':forms.Select(attrs={'class':'form-control'}),
         'current_employer':forms.TextInput(attrs={'class':'form-control','placeholder':'Current company name'}),
         'dob':forms.TextInput(attrs={'class':'form-control','placeholder':'yyyy-mm-dd'}),
         'nearest_city':forms.TextInput(attrs={'class':'form-control'}),
         'preferred_location':forms.TextInput(attrs={'class':'form-control'}),
         'expected_ctc':forms.TextInput(attrs={'class':'form-control','placeholder':'Enter amount in lakhs'}),
          'ctc':forms.TextInput(attrs={'class':'form-control','placeholder':'Enter amount in lakhs'}),
         'current_location':forms.Select(attrs={'class':'form-control'}),
         'corrected_location':forms.Select(attrs={'class':'form-control'}),
         'contact_number':forms.TextInput(attrs={'class':'form-control'}),
         'ug_course':forms.TextInput(attrs={'class':'form-control','placeholder':'BTech/B.E'}),
         'pg_course':forms.TextInput(attrs={'class':'form-control'}),
         'ug_passing_year':forms.Select(attrs={'class':'form-control'}),
         'pg_passing_year':forms.Select(attrs={'class':'form-control'}),
         'work_exp':forms.Select(attrs={'class':'form-control'}),
         'analytics_in_exp':forms.Select(attrs={'class':'form-control'}),
         'address':forms.Textarea(attrs={'class':'form-control','placeholder':'Say Something '}),
         'about_me':forms.Textarea(attrs={'class':'form-control','placeholder':'Say Something '}),
         'pg_institute_name':forms.TextInput(attrs={'class':'form-control'}),'ug_institute_name':forms.TextInput(attrs={'class':'form-control'}),
         'ug_institute_name':forms.TextInput(attrs={'class':'form-control','placeholder':'Osmania University'}),
         'correct_pg_course':forms.TextInput(attrs={'class':'form-control'}),

         # 'tags':forms.TextInput(attrs={'class':'form-control'}),



      }    

   def __init__(self, *args, **kwargs):
      super(JobSeekerProfileForm,self).__init__(*args,**kwargs)
      for fieldname in ['skills']:
            self.fields[fieldname].help_text = 'Enter your Skills'

class JobSeekerMatchingProfileForm(forms.ModelForm):
   class Meta:
      model=JobListing
      fields=['job_skills','job_location','job_min_exp','job_max_exp','job_min_ctc','job_max_ctc']

      labels={
         'job_min_ctc':'Min CTC',
         'job_max_ctc':'Max CTC',
         'job_skills':'Skill',
         'job_location':'Location',
         'job_min_exp':'Min Exp.',
         'job_max_exp':'Max Exp.',
         ##'job_title':'Current Designation'
      }
      

      widgets={
         #'job_location':forms.Select(attrs={'class':'form-control'})
         #'job_min_ctc':forms.Select(attrs={'class':'form-control'}),
         #'job_max_ctc':forms.Select(attrs={'class':'form-control'}),
         #'current_designation':forms.Select(attrs={'class':'form-control'}),



      }


   def __init__(self, *args, **kwargs):
        super(JobSeekerMatchingProfileForm,self).__init__(*args,**kwargs)
        for fieldname in ['job_skills']:
            self.fields[fieldname].help_text =None
            

# class PreferredCandidateForm(ModelForm):
#     ACTION_CHOICE=(
        
#         ('not_interested','Not Interested'),
#         ('interested','Interested'),
#          ('not_answered','Not Answered'),
#         )
#     action_by_recruiter= forms.ChoiceField(choices=ACTION_CHOICE,
#                                 widget=forms.Select(attrs={'class':'selector'}),required=True)
#     class Meta:
#         model=JobSeeker
#         fields=['id','serial_number','name','contact_number','email','action_by_recruiter']



#         widgets={
#             'action_by_recruiter':forms.Select(attrs={'class':'form-control'}),
#             'contact_number':forms.TextInput(attrs={'class':'form-control'}),
#             'name':forms.TextInput(attrs={'class':'form-control'}),
#             'email':forms.TextInput(attrs={'class':'form-control'}),
#             ##'current_designation':forms.Select(attrs={'class':'form-control'}),



#       }


class InterestedPreferredCandidateForm(forms.ModelForm):
    class Meta:
        model=JobSeeker
        fields=['name','email','work_exp','ctc','current_employer','current_designation','current_location','skills','ready_to_relocate','notice_period']



        widgets={
            'current_location':forms.Select(attrs={'class':'form-control'}),
            'current_designation':forms.Select(attrs={'class':'form-control'}),
            'name':forms.TextInput(attrs={'class':'form-control'}),
            'email':forms.EmailInput(attrs={'class':'form-control'}),
            'current_employer':forms.TextInput(attrs={'class':'form-control'}),
            'ctc':forms.TextInput(attrs={'class':'form-control'}),
            'work_exp':forms.TextInput(attrs={'class':'form-control'}),




      }


# class SelectionForm(ModelForm):
#     class Meta:
#         model=JobSeeker
#         fields=['action_by_recruiter']

#         widgets={
#             'action_by_recruiter':forms.Select(attrs={'id':'selection-type','class':'form-control'}),

#         }    
        




      



