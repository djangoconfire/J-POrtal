from rest_framework.serializers import ModelSerializer
from jobs.models import JobListing

class JobListingSerializer(ModelSerializer):
	class Meta:
		model=JobListing
		fields=['job_title','job_min_exp','job_max_exp','job_location','job_min_ctc']
