from django.forms import ModelForm, CheckboxInput ,NumberInput ,DateTimeInput
from django.forms import ModelMultipleChoiceField
from jobs.models import JobListing 
from company.models import Company
#from datetimewidget.widgets import DateTimeWidget
from django.contrib.admin import widgets 
from django import forms
from jobseeker.models import JobSeeker
from django.contrib.admin.widgets import AdminDateWidget 
from django.forms.extras.widgets import SelectDateWidget
from dal import autocomplete

import re
from django.forms.widgets import Widget, Select, MultiWidget
from django.utils.safestring import mark_safe
from pagedown.widgets import PagedownWidget

__all__ = ('SelectTimeWidget', 'SplitSelectDateTimeWidget')

time_pattern = r'(\d\d?):(\d\d)(:(\d\d))? *([aApP]\.?[mM]\.?)?$'

RE_TIME = re.compile(time_pattern)
HOURS = 0
MINUTES = 1
SECONDS = 3
MERIDIEM = 4


class CompanyProfileForm(ModelForm):
    description=forms.CharField(widget=PagedownWidget(show_preview=False))
    class Meta:
        model=Company
        fields=['company_name','company_website','description','company_logo','contact_no','email']

        labels={
          'company_desc':'Brief Writeup on organization'
        }

        widgets={
          'company_name':forms.TextInput(attrs={'class':'form-control'}),
          'company_website':forms.TextInput(attrs={'class':'form-control','placeholder':'http://'}),
          'description':forms.Textarea(attrs={'class':'form-control','placeholder':"Say about company"}),
          'contact_no':forms.TextInput(attrs={'class':'form-control','placeholder':'Enter contact nuber'}),
          'email':forms.EmailInput(attrs={'class':'form-control','placeholder':'example@gmail.com'}),



        }


class FinalShortlistedCandidateForm(ModelForm):
    class Meta:
        model=JobSeeker
        fields=['profile_photo','name','contact_number','email']


class CompanySearchForm(ModelForm):
    

        company = forms.ModelChoiceField(
        queryset=Company.objects.all(),
        widget=autocomplete.ModelSelect2(
            url='/company/company-autocomplete/',
            attrs={
                # Set some placeholder
                'data-placeholder': 'Search Company by name...',
                # Only trigger autocompletion after 3 characters have been typed
                'data-minimum-input-length': 3,
                },
            )
        )
        class Meta:
            model=JobListing
            fields=['company']

            widgets={
                'company':forms.TextInput(attrs={'class':'form-control'}),


                }


        



























        

   
    

    

