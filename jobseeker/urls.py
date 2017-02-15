from django.conf.urls import url,include

from views import *

urlpatterns=[
      
     url(r'^create_profile/$','jobseeker.views.CreateJobSeekerProfile',name="create_jobseeker_profile"),
     url(r'^(?P<slug>[-\w]+)/profile/$','jobseeker.views.JobSeekerProfile',name="profile"),
     url(r'^matching_profile/$','jobseeker.views.MatchingProfile',name="matching_profile"),
     url(r'^searching_matching_profile/$','jobseeker.views.SearchingMatchingProfile',name="searching_matching_profile"),
     url(r'^(?P<slug>[-\w]+)/update/$','jobseeker.views.UpdateProfile',name="update_profile"),
     url(r'^(?P<slug>[-\w]+)/resume/$','jobseeker.views.Resume',name="resume"),
     url(r'^(?P<job_slug>[-\w]+)/preferred_candidate/$','jobseeker.views.PreferredCandidate',name="preferred_candidate"),
     url(r'^(?P<jobseeker_slug>[-\w]+)/(?P<job_slug>[-\w]+)/send_mail/$','jobseeker.views.SendEmail',name="send_mail"),
     url(r'^(?P<job_slug>[-\w]+)/interested_candidate/$','jobseeker.views.InterestedCandidate',name="interested_candidate"),
     url(r'^(?P<company_slug>[-\w]+)/(?P<job_slug>[-\w]+)/shortlisted_candidate/$','jobseeker.views.ShortlistedCandidate',name="shortlisted_candidate"),
     #url(r'^(?P<jobseeker_slug>[-\w]+)/(?P<job_slug>[-\w]+)/shortlisted_candidate/mail$','jobseeker.views.MailToShortlistedCandidate',name="mail_to_shortlisted_candidate"),
     url(r'^(?P<jobseeker_slug>[-\w]+)/(?P<job_slug>[-\w]+)/edit/preferred_candidate/$','jobseeker.views.EditInterestedCandidate',name="edit_interested_candidate"),
     url(r'^(?P<job_slug>[-\w]+)/preferred_interested_candidate/$','jobseeker.views.InterestedPreferredCandidate',name="preferred_interested_candidate"),
     url(r'^selecting_preferred_candidate/$','jobseeker.views.SelectingPreferredCandidate',name="selecting_preferred_candidate"),
     url(r'^send_job_detail/$','jobseeker.views.SendingJobDetail',name="send_job_detail"),
     url(r'^edit_interested_candidate/$','jobseeker.views.EditInterestedCandidate2',name="edit_interested_candidate"),





    ]
