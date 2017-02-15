from django.shortcuts import render

from location.models import City
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

@csrf_exempt
def AddingNewCity(request):
	print 'inside designation'
	if request.method=='POST':
		json_dict={}
		city_name=request.POST.get('city_name','')
		print city_name
		print '***********************'
		new_city=City()
		new_city.city_name=city_name
		try:
			new_city.save()
		except Exception as e:
			return JsonResponse({'success':'False','exception':str(e)})
		json_dict['success']='True'
		json_dict['city_name']=city_name
		return JsonResponse(json_dict)	
	else:
		return JsonResponse({'success':'False','exception':'Not a post request'}) 		

