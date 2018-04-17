function onError(data) {
	//Invalid authorization
	//Display Error Message / Page
	$('body').append(JSON.stringify(data));
}

function onReady(smart) {
	//Page recieves access_token from authorization server
	//Use the access token, and start fetching patient data
	//Access Token is valid for 10 minutes only

	//Access Token
	var token = smart.tokenResponse.access_token;

	//Patient ID
	var patient = smart.tokenResponse.patient;

	//FHIR ENdpoint
	var baseURL = smart.server.serviceUrl;

	var json_data = {};
	json_data.token = token;
	json_data.patient = patient;
	json_data.base_URL = baseURL;

	//Custom Javascript method to make the FHIR queries
	//The method is described in app-script.js
	get_medications(json_data);
}

//Start here
//When page is loaded, the index page recieves code
//This FHIR function, exhanges the code for access_token
FHIR.oauth2.ready(onReady, onError);