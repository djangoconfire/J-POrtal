from django.conf.urls import url,include
from .views import JobDetailApiListView,JobDetailRetrieveApiView,JobCreateApiView
urlpatterns=[

      
      # url(r'^(?P<company_slug>[-\w]+)/(?P<job_slug>[-\w]+)/interview_detail/$','jobs.views.Interview',name="interview_detail"),
      # url(r'^(?P<jobseeker_slug>[-\w]+)/(?P<job_slug>[-\w]+)/apply_job/$','jobs.views.SuccessfullyApplyForJob',name="apply_job"),
      # url(r'^(?P<jobseeker_slug>[-\w]+)/(?P<job_slug>[-\w]+)/description/$','jobs.views.Apply_to_job',name="apply_to_job"),
      # url(r'^(?P<slug>[-\w]+)/edit_job/$','jobs.views.EditJob',name="edit_job"),
      # url(r'^posting_new_job/$','jobs.views.PostingNewJob',name="posting_new_job"),
      # url(r'^preview/$','jobs.views.preview',name="preview"),
      url(r'^$',JobDetailApiListView.as_view(),name="api-jobdetail"),
      url(r'^(?P<company_slug>[-\w]+)/(?P<job_slug>[-\w]+)/job_detail/$',JobDetailRetrieveApiView.as_view(),name="job_detail"),
      # url(r'^(?P<slug>[-\w]+)/edit_job/$',JobUpdateApiView.as_view(),name="edit_job"),
      url(r'^posting_new_job/$',JobCreateApiView.as_view(),name="posting_new_job"),


    ]
