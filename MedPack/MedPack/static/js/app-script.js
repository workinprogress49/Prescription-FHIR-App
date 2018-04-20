Array.prototype.removeValue = function(name, value){
   var array = $.map(this, function(v,i){
      return v[name] != value ? null : v;
   });
   this.length = 0; //clear original array
   this.push.apply(this, array); //push all elements except the one we want to delete
}


function get_medications(json_data) {
	$.ajax({
		url: "/medications/",
		type: 'POST',
		data: JSON.stringify(json_data),
		contentType: 'application/json; charset=utf-8',
		dataType: "json",
		success: function (data) {
			//data contains the json object for the data table
			//Send the data to DataTables
			$('#medication-table2').DataTable({
				"data": data,
			    paging: false,
			    destroy: true,//This needs to be here since we had already established the original datatable with an id
				"columns": [
					{"data": "Medication"},
					{"data": "Frequency"},
					{"data": "Start Date"},
					{"data": "End Date"},
					{"data": "Date Added"},
					{"data": "Status"},
					{"data": "Duration"},
					{"data": "Dose per Day"}
				]
			});

			data.removeValue('Status','active')

			$('#medication-table').DataTable({
				"data": data,
			    paging: false,
			    destroy: true,//This needs to be here since we had already established the original datatable with an id
				"columns": [
					{"data": "Medication"},
					{"data": "Frequency"},
					{"data": "Start Date"},
					{"data": "End Date"},
					{"data": "Date Added"},
					{"data": "Status"},
					{"data": "Duration"},
					{"data": "Dose per Day"}
				]
			});
		},
		error: function (data) {
			//Error from /medication URL
			//Display error message /error page
			$('body').append(JSON.stringify(data))
		}
	});
}