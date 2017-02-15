from rest_framework.generics import ListAPIView,RetrieveAPIView,CreateAPIView
from jobs.models import JobListing
from serializers import JobListingSerializer


class JobDetailApiListView(ListAPIView):
	queryset=JobListing.objects.all()
	serializer_class=JobListingSerializer

class JobCreateApiView(CreateAPIView):
	queryset=JobListing.objects.all()
	serializer_class=JobListingSerializer



class JobDetailRetrieveApiView(RetrieveAPIView):
	queryset=JobListing.objects.all()
	serializer_class=JobListingSerializer
	lookup_field="slug"


# class JobUpdateApiView(UpdateAPIView):
# 	queryset=JobListing.objects.all()
# 	serializer_class=JobListingSerializer



# class JobDeleteApiView(DeleteAPIView):
# 	queryset=JobListing.objects.all()
# 	serializer_class=JobListingSerializer



