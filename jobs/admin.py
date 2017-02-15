from django.contrib import admin

# Register your models here.
from django.contrib import admin

from models import JobListing,JobApplications,InterviewDetail,PreferredCandidate,MailToShortlisted,ShortlistedCandidates
from user_profile.models import UserProfile
admin.site.register(JobListing)
admin.site.register(UserProfile)
class JobApplicationAdmin(admin.ModelAdmin):
	list_display = ('job','jobseeker',)
admin.site.register(JobApplications,JobApplicationAdmin)
admin.site.register(InterviewDetail)
admin.site.register(PreferredCandidate)
admin.site.register(MailToShortlisted)
admin.site.register(ShortlistedCandidates)
##admin.site.register(SkillsRequired)