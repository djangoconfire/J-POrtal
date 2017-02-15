from django.contrib import admin

from company.models import *
from jobs.models import MailToCompany



admin.site.register(Company)

admin.site.register(MailToCompany)



