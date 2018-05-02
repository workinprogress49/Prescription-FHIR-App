from django.views.decorators.csrf import csrf_exempt
from django.template.response import TemplateResponse
from django.http import JsonResponse, HttpResponse
import json
import requests
import traceback
from datetime import datetime
from flatten_json import flatten


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
			data = r.json()

			output = []
			current = []

			timing_value ={'alt. d.':0.5,'Alt. D.':0.5,'EOD':0.5,'q.a.d':0.5,'Daily':1,'ind.':1,'QD':1,'qd':1,'hor. decub.':1,'mane':1,'noct.':1,'o.d.':1,'o.m.':1,'o.n.':1,'OPD':1,'p.m.':1,'q.a.m.':1,'q.d.a.m.':1,'q.d.p.m.':1,'q.p.m.':1,'s.i.d.':1,'b.i.d.':2,'BID':2,'bis ind.':2,'BDS':2,'b.d.s.':2,'TID':3,'t.d.s.':3,'TDS':3,'QID':4,'q.d.s.':6,'q.q.h.':6,'hor. tert.':8,'alt. h.':12,'hor. alt.':12,'omn. bih.':12,'omn. hor.':24,'q.h.':24,'q12hr':2,'q2hr':12,'q4hr':6,'q6hr':4,'q8hr':3,'qhr':24}


			date_only = lambda x : x.split('T')[0] if x != 'N/A' else x
			show_month = lambda x : datetime.strptime(x,'%Y-%m-%d').strftime('%Y-%B-%d') if x != 'N/A' else x

			for i in range(len(data['entry'])):
				flat_earth = flatten(data['entry'][i])
				row = {
					'Medication' : flat_earth.get('resource_medicationCodeableConcept_text','N/A'),
					'Frequency' : flat_earth.get('resource_dosage_0_text','N/A'),
					'Start Date' : show_month(date_only(flat_earth.get('resource_effectivePeriod_start','N/A'))),
					'End Date': show_month(date_only(flat_earth.get('resource_effectivePeriod_end','N/A'))),
					'Date Added' : show_month(date_only(flat_earth.get('resource_dateAsserted','N/A'))),
					'Status' : flat_earth.get('resource_status','N/A')
					  }

				if row['Start Date'] != 'N/A' and row['End Date'] != 'N/A':
					row['Duration'] = str((datetime.strptime(row['End Date'], '%Y-%B-%d') - datetime.strptime(row['Start Date'], '%Y-%B-%d')).days) + ' days'
				else:
					row['Duration'] = 'Ongoing'

				if timing_value.get(flat_earth.get('resource_dosage_0_timing_code_text','N/A'), 'N/A') != 'N/A' and flat_earth.get('resource_dosage_0_quantityQuantity_value','N/A') != 'N/A':
					row['Dose per Day'] = str(timing_value.get(flat_earth.get('resource_dosage_0_timing_code_text','N/A'), 'N/A') * flat_earth.get('resource_dosage_0_quantityQuantity_value','N/A')) + flat_earth.get('resource_dosage_0_quantityQuantity_unit','N/A')
				else:
					row['Dose per Day'] = 'N/A'
				output.append(row)

			for i in output:
				if i['Status'] == 'active':
					current.append(i)

		else:
			output = {'error': r.headers['Status']}

		return JsonResponse(output, safe=False)

	except:
		e = traceback.format_exc()
		data = {'error':str(e)}
		return JsonResponse(e)
