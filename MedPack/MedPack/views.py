from django.views.decorators.csrf import csrf_exempt
from django.template.response import TemplateResponse
from django.http import JsonResponse, HttpResponse
import json
import requests
import traceback
import math
import pandas as pd
from datetime import datetime


def home(request):
	return TemplateResponse(request, 'home.html', {})

def launch(request):
	return TemplateResponse(request,'launch.html', {})

@csrf_exempt
def medications(request):
    #input = json.loads(request.body.decode('utf-8'))
    input = json.loads(request.body)
    #return HttpResponse(input, content_type='application/json')


    fhir_endpoint = input['base_URL']

    headers = {'Accept': 'application/json+fhir', 'Authorization': 'Bearer ' + input["token"]}

    resource = "MedicationStatement"
    parameters = {"patient": input["patient"]}

    query_url = fhir_endpoint + '/' + resource

    try:
    	r = requests.get(query_url, params=parameters, headers=headers)
    	if (r.status_code == 200):
    		data = r.json
    		output = []

    		i = 0
    		while i < 10:
    			row = {'medication': 'Med' + str(i), 'start': 'Start' + str(i), 'quantity':'Quantity'+str(i)}
    			output.append(row)
    			i +=  1

    	else:
    		output = {'error': r.headers['Status']}

    	return JsonResponse(output, safe=False)

    except:
    	e = traceback.format_exc()
    	data = {'error':str(e)}
    	return JsonResponse(e)
