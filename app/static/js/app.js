var table = null;

$(document).ready(function () {
	getTraingData([], null);
	getSeminorData([], null);
	getLinkingData([], null);
	document.getElementById("defaultOpen").click();
});

function openCity(evt, cityName) {
    var i, tabcontent, tablinks;
    tabcontent = document.getElementsByClassName("tabcontent");
    for (i = 0; i < tabcontent.length; i++) {
        tabcontent[i].style.display = "none";
    }
    tablinks = document.getElementsByClassName("tablinks");
    for (i = 0; i < tablinks.length; i++) {
        tablinks[i].className = tablinks[i].className.replace(" active", "");
    }
    document.getElementById(cityName).style.display = "block";
    evt.currentTarget.className += " active";
}

function getTraingData(rows, cursor) {

	var url = "/admin/report/training?";
    if(cursor) url += "cursor=" + cursor;

	$.ajax({
		url: url,
		}).done(function( data ) {
		    rows = rows.concat(data.data);
		    if(data.more){
		        getTraingData(rows, data.cursor);
		    } else {
		        initTraingTable(rows);
		    }
		});
}

function initTraingTable(rows) {
	table = $('#table_training').DataTable({
		responsive: true,
		data: rows,
		"pageLength": 20,
		"order": [[ 5, "asc" ]],
		 columns: [
		 	{data: 'title'},
		    {data: 'first_name'},
		    {data: 'last_name'},
		    {data: 'id_number'},
		    {data: 'cellphone'},
		    {data: 'reference_number'},
		    {data: 'city'},
		    {data: 'date'},
		    {data: 'reffered_by_name'},
		    {data: 'reffered_by_surname'},
		    {data: 'reffered_by_contact'}
		    ],
		    dom: 'Bfrtip',
		   	buttons: [
            	{ extend: 'excel', 
            	  text: 'Download Excel Sheet',
            	  filename: function(){
                						var date = new Date();
                						var day = date.getDate();
                						var month = date.getMonth();
                						var year = date.getFullYear();
               				 			return 'Training Members' + day +'-'+ month +'-' + year;
            						}
            	}
        	]
		});
}

function getSeminorData(rows, cursor) {

	var url = "/admin/report/seminor?";
    if(cursor) url += "cursor=" + cursor;

	$.ajax({
		url: url,
		}).done(function( data ) {
		    rows = rows.concat(data.data);
		    if(data.more){
		        getSeminorData(rows, data.cursor);
		    } else {
		        initSeminorTable(rows);
		    }
		});
}

function initSeminorTable(rows) {
	table = $('#table_seminor').DataTable({
		responsive: true,
		data: rows,
		"pageLength": 20,
		"order": [[ 1, "asc" ]],
		 columns: [
		 	{data: 'title'},
		    {data: 'first_name'},
		    {data: 'last_name'},
		    {data: 'id_number'},
		    {data: 'cellphone'},
		    {data: 'reference_number'},
		    {data: 'reffered_by_name'},
		    {data: 'reffered_by_surname'},
		    {data: 'reffered_by_contact'}
		    ],
		    dom: 'Bfrtip',
		   	buttons: [
            	{ extend: 'excel', 
            	  text: 'Download Excel Sheet',
            	  filename: function(){
                						var date = new Date();
                						var day = date.getDate();
                						var month = date.getMonth();
                						var year = date.getFullYear();
               				 			return 'Seminor Members' + day +'-'+ month +'-' + year;
            						}
            	}
        	]
		});
}

function getRegistrationData(rows, cursor) {

	var url = "/admin/report/register?";
    if(cursor) url += "cursor=" + cursor;

	$.ajax({
		url: url,
		}).done(function( data ) {
		    rows = rows.concat(data.data);
		    if(data.more){
		        getRegistrationData(rows, data.cursor);
		    } else {
		        initRegistrationTable(rows);
		    }
		});
}

function initRegistrationTable(rows) {
	table = $('#table_registration').DataTable({
		responsive: true,
		data: rows,
		"pageLength": 20,
		"order": [[ 1, "asc" ]],
		 columns: [
		 	{data: 'title'},
		    {data: 'first_name'},
		    {data: 'last_name'},
		    {data: 'id_number'},
		    {data: 'cellphone'},
		    {data: 'reffered_by_name'},
		    {data: 'reffered_by_surname'},
		    {data: 'reffered_by_contact'}
		    ],
		    dom: 'Bfrtip',
		   	buttons: [
            	{ extend: 'excel', 
            	  text: 'Download Excel Sheet',
            	  filename: function(){
                						var date = new Date();
                						var day = date.getDate();
                						var month = date.getMonth();
                						var year = date.getFullYear();
               				 			return 'Registered Members' + day +'-'+ month +'-' + year;
            						}
            	}
        	]
		});
}

function getLinkingData(rows, cursor) {

	var url = "/admin/report/linking?";
    if(cursor) url += "cursor=" + cursor;

	$.ajax({
		url: url,
		}).done(function( data ) {
		    rows = rows.concat(data.data);
		    if(data.more){
		        getLinkingData(rows, data.cursor);
		    } else {
		        initLinkingTable(rows);
		    }
		});
}

function initLinkingTable(rows) {
	table = $('#table_linking').DataTable({
		responsive: true,
		data: rows,
		"pageLength": 20,
		"order": [[ 1, "asc" ]],
		 columns: [
		 	{data: 'title'},
		    {data: 'first_name'},
		    {data: 'last_name'},
		    {data: 'id_number'},
		    {data: 'cellphone'},
		    {data: 'reference_number'},
		    {data: 'reffered_by_name'},
		    {data: 'reffered_by_surname'},
		    {data: 'reffered_by_contact'}
		    ],
		    dom: 'Bfrtip',
		   	buttons: [
            	{ extend: 'excel', 
            	  text: 'Download Excel Sheet',
            	  filename: function(){
                						var date = new Date();
                						var day = date.getDate();
                						var month = date.getMonth();
                						var year = date.getFullYear();
               				 			return 'Linking Members' + day +'-'+ month +'-' + year;
            						}
            	}
        	]
		});
}