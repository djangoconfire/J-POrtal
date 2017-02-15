import sys,os,django
from decimal import Decimal

sys.path.append("/home/ritu/Desktop/Projects/Django/jobs_portal/analytics/analytics") #Set it to the root of your project
os.environ["DJANGO_SETTINGS_MODULE"] = "analytics.settings"
django.setup()

import csv



# Full path and name to your csv file
csv_filepathname="/home/ritu/Desktop/Projects/Django/jobs_portal/analytics/analytics/jobseekers.csv"
# Full path to your django project directory
your_project_home="/home/ritu/Desktop/Projects/Django/jobseeker.csv"


from location.models import City,CorrectedCity
from django.conf import settings



with open(csv_filepathname) as csv_file:
    dataReader = csv.reader(csv_file, delimiter=',', quotechar='"')

    for row in dataReader:
        city=City.objects.get_or_create(city_name=row[7])
        corrected_city=CorrectedCity.objects.get_or_create(city_name=row[8])
        #city.city_name=row[8]
        ##print(city)

        #city.save()
        