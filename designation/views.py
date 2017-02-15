from django.shortcuts import render

from designation.models import Designation
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

@csrf_exempt
def AddingNewDesignation(request):
	print 'inside designation'
	if request.method=='POST':
		json_dict={}
		designation_name=request.POST.get('designation_name','')
		print designation_name
		print '***********************'
		new_designation=Designation()
		new_designation.position=designation_name
		try:
			new_designation.save()
		except Exception as e:
			return JsonResponse({'success':'False','exception':str(e)})
		json_dict['success']='True'
		json_dict['designation_name']=designation_name
		return JsonResponse(json_dict)	
	else:
		return JsonResponse({'success':'False','exception':'Not a post request'}) 		

