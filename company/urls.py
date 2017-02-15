from django.conf.urls import url,include

from views import *

urlpatterns=[
      
      url(r'^(?P<slug>[-\w]+)/full_detail/$','company.views.ViewFullDetail',name="full_detail"),
      url(r'^create_profile/$','company.views.CreateCompanyProfile',name="create_profile"),
      url(r'^search/$','company.views.search',name="search"),
      url(r'^(?P<company_slug>[-\w]+)/(?P<job_slug>[-\w]+)/mail/$','company.views.SendingMailToCompany',name="mail_to_company"),
      url(r'^(?P<slug>[-\w]+)/update/$','company.views.UpdateCompanyProfile',name="update_profile"),
      url(r'^(?P<company_slug>[-\w]+)/posted_job/$','company.views.PostedJobByCompany',name="posted_job"),
      url(r'^(?P<company_slug>[-\w]+)/(?P<job_slug>[-\w]+)/job_detail/$','company.views.JobDetail',name="job_detail"),
      url(r'^candidate_selection$','company.views.CandidateSelection',name="candidate_selection"),
      url(r'^candidate_rejection$','company.views.CandidateRejection',name="candidate_rejection"),
      url(r'^(?P<company_slug>[-\w]+)/(?P<job_slug>[-\w]+)/final_shortlisted_candidates$','company.views.FinalShortlistedCandidates',name="final_shortlisted_candidates"),
      url(r'^see_more$','company.views.SeeMore',name="see_more"),
      url(r'^preview/$','company.views.preview',name="preview"),
  
      url(
        r'^company-autocomplete/$',
        CompanyAutocomplete.as_view(),
        name='company-autocomplete',
      ),

      url(r'^final_shortlisted_candidates/$','company.views.ShortlistedCandidates',name="final_shortlisted"),
      url(r'^(?P<company_slug>[-\w]+)/(?P<job_slug>[-\w]+)/company_shortlisted_candidates$','company.views.CompanyShortlistedCandidates',name="company_shortlisted_candidates"),
      


    ]
