function get_medications(json_data) {
	$.ajax({
		url: "/medications/",
		type: 'POST'
		data: JSON.stringify(json_data),
		contentType: 'application/json; charset=utf-8',
		dataType: "json",
		success: function (data) {
			//data contains the json object for the data table
			//Send the data to DataTables
			$('#medication-table').DataTable({
				"data": data,
				"columns": [
				{"data": "medication"},
				{"data": "start"},
				{"data": "quantity"}
				]
			});
		},
		error function (data) {
			//Error from /medication URL
			//Display error message /error page
			$('body').append(JSON.stringify(data))
		}
	})
}