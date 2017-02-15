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


from jobseeker.models import JobSeeker
from django.conf import settings
from taggit.models import Tag
from location.models import City,CorrectedCity
from designation.models import Designation

## for adding location to jobseeker
cities = City.objects.all()
tempMap = {}
for city in cities:
    tempMap[city.city_name]=city
print(tempMap)


corrected_cities = CorrectedCity.objects.all()
tempMap_2 = {}
for city in corrected_cities:
    tempMap_2[city.city_name]=city
print(tempMap_2)


## for adding designation to jobseeker
designation = Designation.objects.all()
tempMap_3 = {}

for designation in designation:
    tempMap_3[designation.position]=designation
print(tempMap_3)

with open(csv_filepathname) as csv_file:
    dataReader = csv.reader(csv_file, delimiter=',', quotechar='"')

    for row in dataReader:
        jobseeker=JobSeeker()
        jobseeker.serial_number=row[0]
        jobseeker.resume2=row[1]
        jobseeker.name=row[2]
        jobseeker.contact_number=row[3]
        jobseeker.email=row[4]
        jobseeker.work_exp=Decimal(row[5])
        if row[6]:
            jobseeker.analytics_in_exp=Decimal(row[6])
        else:
            pass    
        print(row[7],row[8])
        if len(row[7])>0:
            cLoc = row[7]
            if(cLoc in  tempMap.keys()):
                print(row[2],row[7])
                jobseeker.current_location=tempMap[cLoc]
            else:
                pass
        # if len(row[8])>0:
        #     correctedLoc = row[8]
        #     if(correctedLoc in  tempMap_2.keys()):
        #         print(row[2],row[8])
        #         jobseeker.corrected_location=tempMap_2[correctedLoc]
        #     else:
        #         pass        

        jobseeker.nearest_city=row[9]
        jobseeker.preferred_location=row[10]
        jobseeker.ctc=row[11]
        jobseeker.current_employer=row[12]
        if row[13]:
            cdesignation = row[13]
            if(cdesignation in  tempMap_3.keys()):
                #print(row[2],row[13])
                jobseeker.current_designation=tempMap_3[cdesignation]
            else:
                pass

        skill_data=row[14]

        list_of_skills = skill_data.strip().split(',')
        #print '\n\n\n'
        #print list_of_skills
        for skill in list_of_skills:
            if skill != '' and skill != None:
                try:
                    skill_tag = Tag.objects.get(name=skill)
                    jobseeker.skills.add(skill_tag) 
                except:
                    pass
            jobseeker.save()        

                    
               

                
        
        jobseeker.ug_course=row[15]
        jobseeker.ug_course2=row[16]
        jobseeker.ug_institute_name=row[17]
        jobseeker.tier1=row[18]
        jobseeker.ug_passing_year=row[19]
        jobseeker.pg_course=row[20]
        jobseeker.correct_pg_course=row[20]
        jobseeker.pg_institute_name=row[21]
        jobseeker.pg_tier1=row[22]
        jobseeker.pg_passing_year=row[23]

        jobseeker.save()
        