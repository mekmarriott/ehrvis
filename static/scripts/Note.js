

var Note = {};
Note.base = 1;
Note.step = 0.2;
Note.curr_preview = "";
Note.curr_type = "";
Note.curr_service = "";
Note.curr_timestamp = "";
Note.curr_fulltext = "";
Note.curr_noteID = 0;


// data format: [ { data: ---, label: ---}, {data: ----, label: ---}, ... ]
Note.plotData = [];


// plotting options for main timeline
Note.plot_min = 0;
Note.plot_max = 1;
Note.plotOptions = {};
Note.plotOptions.series = { lines: {show: false}, points: {show: true }};
Note.plotOptions.grid = { hoverable: true, clickable: true, markings: [] };
Note.plotOptions.yaxis = { min: 0, autoscaleMargin: 0.5 }; 
Note.plotOptions.xaxis = { min: 0, max: 1, mode: "time" };

// plotting options for navigation strip

Note.navOptions = {};
Note.navOptions.series = { lines: {show: false}, points: {show: true }};
Note.navOptions.grid = { hoverable: true, clickable: true, markings: [] };
Note.navOptions.yaxis = { min: 0, autoscaleMargin: 0.5 }; 
Note.navOptions.xaxis = { min: 0, max: 1, mode: "time" };


		// var sin = [],
		// 	cos = [];

		// for (var i = 0; i < 14; i += 0.5) {
		// 	sin.push([i, Math.sin(i)]);
		// 	cos.push([i, Math.cos(i)]);
		// }

		// var plot = $.plot("#placeholder", [
		// 	{ data: sin, label: "sin(x)"},
		// 	{ data: cos, label: "cos(x)"}
		// ], 


function createNoteTimeline(noteSeries, hospitalStays, minDate, maxDate){


	// for now...
	return

	// assign dataseries:
	Note.plotData = noteSeries;
	
	// convert heighcounts to heights
	for (var i = Note.plotData.length - 1; i >= 0; i--) {
		height_conversion(Note.plotData[i].data)
	};


	//TODO: CONVERT TIMESTAMPS

	// set main plot window to [t_max-90days,t_max] by default
	Note.plotOptions.xaxis.min = maxDate - 90 * (24 * 60 * 60 * 1000);
	Note.plotOptions.xaxis.max = maxDate;
	// set nav plot window to [t_min, t_max] permanently
	Note.plotOptions.xaxis.min = minDate;
	Note.plotOptions.xaxis.max = maxDate;

	// mark hospital stays
	for (var i = hospitalStays.length - 1; i >= 0; i--) {
		Note.plotOptions.grid.markings.push({ xaxis: { from: hospitalStays[i][0], to: hospitalStays[i][1]} });
	}

	// plot dataseries
	 $.plot("#note_plot_target", Note.plotData, Note.plotOptions);
	 $.plot("#note_nav_target", Note.plotData, Note.navOptions);


	// create tooltip div 
	$("<div id='note_tooltip'></div>").css({
		position: "absolute",
		display: "none",
		border: "1px solid #fdd",
		padding: "2px",
		"background-color": "#fee",
		opacity: 1.0
	}).appendTo("body");


    //Bind tooltip to plot
    $("#note_plot_target").bind("plothover", function (event, pos, item) {
      if (item) {
        var t = item.datapoint[0],
          h = item.datapoint[1];

        // set tooltip contents
        set_preview_data(t,h)

        // $("#tooltip").html("<strong>Percentile:</strong> " + y + "<br><strong> Dose: </strong> " + x + " Gy")
        $("#note_tooltip").html(Note.curr_timestamp + "<br><strong> Type: </strong> " + Note.curr_type + "<br><strong> Service: </strong> " + Note.curr_service + "<br><br><strong> Preview: </strong>" + Note.curr_preview)
          .css({top: item.pageY+5, left: item.pageX+5})
          .fadeIn(200);
      } else {
        $("#note_tooltip").hide();
      }
    });

	//Hide tooltip div when mouse leaves note plot panel
	$("#note_plot_target").mouseleave(function(){
		$("#note_tooltip").hide();     
	});

}


function count2height(count){
	return Note.base + Note.step*(count-1);
}

function height2count(height){
	return parseInt((height - Note.base)/Note.step) + 1;
}

function height2arrayidx(height){
	return parseInt((height - Note.base)/Note.step);
}

function height_conversion(data_array){
	// data array expected to be in form [ [ date_1, count_1] , [date_2,count_2] , ... ]
	for (var i = data_array.length - 1; i >= 0; i--) {

		// for ith [date,count] pair, get second value (index 1), convert count to height
		data_array[i][1]=count2height(data_array[i][1]);
	};
}


function set_preview_data(date,height){
	idx = height2arrayidx(height);
	Note.curr_preview = note_dictionary[date][idx]['preview'];
	Note.curr_service = note_dictionary[date][idx]['service'];
	Note.curr_type = note_dictionary[date][idx]['type'];
	Note.curr_timestamp = note_dictionary[date][idx]['time'];
	Note.curr_noteID = note_dictionary[date][idx]['id'];

}

function get_fulltext_byID(note_id){
	var text;
	$.getJSON( "/_note/" + note_id, function(result) {
		console.log(result);
		text= result.fulltext;
	});
	return text;
}

function get_fulltext(date,height){
	idx = height2arrayidx(height);
	return get_fulltext_byindex(note_dictionary[date][idx]['id']);
}





