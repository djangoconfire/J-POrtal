from django import forms
from dal import autocomplete
from django.forms import ModelForm

from .models import JobListing,InterviewDetail
from company.models import Company
from django.contrib.admin.widgets import AdminDateWidget 
from django.forms.extras.widgets import SelectDateWidget

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

#from tinymce.widgets import TinyMCE



class JobCreatingForm(forms.ModelForm):
    company = forms.ModelChoiceField(
        queryset=Company.objects.all(),
        widget=autocomplete.ModelSelect2(
            url='/company/company-autocomplete/',
            attrs={
                # Set some placeholder
                'data-placeholder': 'Enter a company name...',
                # Only trigger autocompletion after 3 characters have been typed
                'data-minimum-input-length': 3,
                },
            )
    )

    job_desc=forms.CharField(widget=PagedownWidget(show_preview=False))

    pub_date=forms.DateField(widget=forms.SelectDateWidget)
    JOB_TYPE_CHOICES = [
            ('fulltime','Full Time'),
            ('contract','Contract'),
            ('intern','Intern'),
            ('freelance','Freelance'),
            ('parttime','Part Time')
    ]

    #job_desc=forms.CharField(widget=TinyMCE(attrs={'cols': 80, 'rows': 10}))

    class Meta:
    	model=JobListing
    	fields=['company','job_title','job_type','job_desc','job_location','job_min_ctc','job_max_ctc','job_min_exp','job_max_exp','pub_date','job_skills']
    	

        labels={
         'job_title':'Job Title',
         'job_type':'Job Type',
         'job_desc':'Description',
         'job_min_ctc':'Min CTC.',
         'job_max_ctc':'Max CTC.',
         'job_min_exp':'Min Exp.',
         'job_max_exp':'Max Exp.',
         'job_skills': 'Skills Required',
         'job_location':'Location',
         'pub_date': 'Published on '

        }


        widgets={
          'job_title':forms.Select(attrs={'class':'form-control'}),
          'job_type':forms.Select(attrs={'class':'form-control'}),
          'job_min_exp':forms.Select(attrs={'class':'form-control'}),
          'job_max_exp':forms.Select(attrs={'class':'form-control'}),
          'job_min_ctc':forms.Select(attrs={'class':'form-control'}),
          'job_max_ctc':forms.Select(attrs={'class':'form-control'}),
          'job_location':forms.Select(attrs={'class':'form-control'}),
          'company':forms.TextInput(attrs={'class':'form-control'}),
          'job_desc':forms.Textarea(attrs={'class':'form-control','placeholder':"Say about company"}),
          'pub_date' :forms.SelectDateWidget(attrs={'class':'form-control'})


        }





    def __init__(self, *args, **kwargs):
        super(JobCreatingForm,self).__init__(*args,**kwargs)
        for fieldname in ['job_skills']:
            self.fields[fieldname].help_text =None


            
class SelectTimeWidget(Widget):
    """
    A Widget that splits time input into <select> elements.
    Allows form to show as 24hr: <hour>:<minute>:<second>, (default)
    or as 12hr: <hour>:<minute>:<second> <am|pm> 
    
    Also allows user-defined increments for minutes/seconds
    """
    hour_field = '%s_hour'
    minute_field = '%s_minute'
    second_field = '%s_second' 
    meridiem_field = '%s_meridiem'
    twelve_hr = False # Default to 24hr.
    
    def __init__(self, attrs=None, hour_step=None, minute_step=None, second_step=None, twelve_hr=False):
        """
        hour_step, minute_step, second_step are optional step values for
        for the range of values for the associated select element
        twelve_hr: If True, forces the output to be in 12-hr format (rather than 24-hr)
        """
        self.attrs = attrs or {}
        
        if twelve_hr:
            self.twelve_hr = True # Do 12hr (rather than 24hr)
            self.meridiem_val = 'a.m.' # Default to Morning (A.M.)
        
        if hour_step and twelve_hr:
            self.hours = range(1,13,hour_step) 
        elif hour_step: # 24hr, with stepping.
            self.hours = range(0,24,hour_step)
        elif twelve_hr: # 12hr, no stepping
            self.hours = range(1,13)
        else: # 24hr, no stepping
            self.hours = range(0,24) 

        if minute_step:
            self.minutes = range(0,60,minute_step)
        else:
            self.minutes = range(0,60)

        if second_step:
            self.seconds = range(0,60,second_step)
        else:
            self.seconds = range(0,60)

    def render(self, name, value, attrs=None):
        try: # try to get time values from a datetime.time object (value)
            hour_val, minute_val, second_val = value.hour, value.minute, value.second
            if self.twelve_hr:
                if hour_val >= 12:
                    self.meridiem_val = 'p.m.'
                else:
                    self.meridiem_val = 'a.m.'
        except AttributeError:
            hour_val = minute_val = second_val = 0
            if isinstance(value, basestring):
                match = RE_TIME.match(value)
                if match:
                    time_groups = match.groups();
                    hour_val = int(time_groups[HOURS]) % 24 # force to range(0-24)
                    minute_val = int(time_groups[MINUTES]) 
                    if time_groups[SECONDS] is None:
                        second_val = 0
                    else:
                        second_val = int(time_groups[SECONDS])
                    
                    # check to see if meridiem was passed in
                    if time_groups[MERIDIEM] is not None:
                        self.meridiem_val = time_groups[MERIDIEM]
                    else: # otherwise, set the meridiem based on the time
                        if self.twelve_hr:
                            if hour_val >= 12:
                                self.meridiem_val = 'p.m.'
                            else:
                                self.meridiem_val = 'a.m.'
                        else:
                            self.meridiem_val = None
                    

        # If we're doing a 12-hr clock, there will be a meridiem value, so make sure the
        # hours get printed correctly
        if self.twelve_hr and self.meridiem_val:
            if self.meridiem_val.lower().startswith('p') and hour_val > 12 and hour_val < 24:
                hour_val = hour_val % 12
        elif hour_val == 0:
            hour_val = 12
            
        output = []
        if 'id' in self.attrs:
            id_ = self.attrs['id']
        else:
            id_ = 'id_%s' % name

        # For times to get displayed correctly, the values MUST be converted to unicode
        # When Select builds a list of options, it checks against Unicode values
        hour_val = u"%.2d" % hour_val
        minute_val = u"%.2d" % minute_val
        second_val = u"%.2d" % second_val

        hour_choices = [("%.2d"%i, "%.2d"%i) for i in self.hours]
        local_attrs = self.build_attrs(id=self.hour_field % id_)
        select_html = Select(choices=hour_choices).render(self.hour_field % name, hour_val, local_attrs)
        output.append(select_html)

        minute_choices = [("%.2d"%i, "%.2d"%i) for i in self.minutes]
        local_attrs['id'] = self.minute_field % id_
        select_html = Select(choices=minute_choices).render(self.minute_field % name, minute_val, local_attrs)
        output.append(select_html)

        second_choices = [("%.2d"%i, "%.2d"%i) for i in self.seconds]
        local_attrs['id'] = self.second_field % id_
        select_html = Select(choices=second_choices).render(self.second_field % name, second_val, local_attrs)
        output.append(select_html)
    
        if self.twelve_hr:
            #  If we were given an initial value, make sure the correct meridiem gets selected.
            if self.meridiem_val is not None and  self.meridiem_val.startswith('p'):
                    meridiem_choices = [('p.m.','p.m.'), ('a.m.','a.m.')]
            else:
                meridiem_choices = [('a.m.','a.m.'), ('p.m.','p.m.')]

            local_attrs['id'] = local_attrs['id'] = self.meridiem_field % id_
            select_html = Select(choices=meridiem_choices).render(self.meridiem_field % name, self.meridiem_val, local_attrs)
            output.append(select_html)

        return mark_safe(u'\n'.join(output))

    def id_for_label(self, id_):
        return '%s_hour' % id_
    id_for_label = classmethod(id_for_label)

    def value_from_datadict(self, data, files, name):
        # if there's not h:m:s data, assume zero:
        h = data.get(self.hour_field % name, 0) # hour
        m = data.get(self.minute_field % name, 0) # minute 
        s = data.get(self.second_field % name, 0) # second

        meridiem = data.get(self.meridiem_field % name, None)

        #NOTE: if meridiem is None, assume 24-hr
        if meridiem is not None:
            if meridiem.lower().startswith('p') and int(h) != 12:
                h = (int(h)+12)%24 
            elif meridiem.lower().startswith('a') and int(h) == 12:
                h = 0
        
        if (int(h) == 0 or h) and m and s:
            return '%s:%s:%s' % (h, m, s)

        return data.get(name, None)







class InterviewDetailForm(ModelForm):
    date_of_interview = forms.CharField(
    widget=SelectDateWidget(
        empty_label=("Choose Year", "Choose Month", "Choose Day"),
    ),
    )

    time_start = forms.CharField(widget=SelectTimeWidget(twelve_hr=True))
    time_end = forms.CharField(widget=SelectTimeWidget(twelve_hr=True))
    class Meta:
        model=InterviewDetail
        fields=['date_of_interview','time_start','time_end','interview_choice']


        def __init__(self, *args, **kwargs):
            super(InterviewDetailForm, self).__init__(*args, **kwargs)
            self.fields['date_of_interview'].widget = widgets.AdminDateWidget()
            self.fields['time_start'].widget = widgets.AdminTimeWidget()
            ##self.fields['mydatetime'].widget = widgets.AdminSplitDateTime()


        widgets={
        'interview_choice':forms.Select(attrs={'class':'form-control'}),

        }
        





