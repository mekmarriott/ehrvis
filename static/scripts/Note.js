

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

unix_month = 904400

// plotting options for main timeline
Note.plot_min = 0;
Note.plot_max = 1;
Note.plotOptions = {};
Note.plotOptions.series = { lines: {show: false}, points: {show: true }};
Note.plotOptions.grid = { hoverable: true, markings: [] };
Note.plotOptions.yaxis = { min: 1-0.1, autoscaleMargin: 0.1, zoomRange: false, ticks: [], panRange: false }; 
Note.plotOptions.xaxis = { min: 0, max: 1, mode: "time", zoomRange: [1,null], panRange: [0,1] };
Note.plotOptions.zoom = { interactive: true };
Note.plotOptions.pan = { interactive: true }; 


// plotting options for navigation strip

Note.navOptions = {};
Note.navOptions.series = { lines: {show: false}, points: {show: true }};
Note.navOptions.grid = { hoverable: true, markings: [] };
Note.navOptions.yaxis = { min: 1-0.1, autoscaleMargin: 0.1, ticks: [], panRange: false }; 
Note.navOptions.xaxis = { min: 0, max: 1, mode: "time", ticks: [], panRange: [0,1] };
Note.navOptions.shift = { interactive: true };



function createNoteTimeline(noteSeries, hospitalStays, minDate, maxDate){

	// assign dataseries:
	Note.plotData = noteSeries;
	
	// convert heighcounts to heights
	for (var i = Note.plotData.length - 1; i >= 0; i--) {
		height_conversion(Note.plotData[i].data)
	};

	// TODO:  GET RID OF NAV PLOT LEGEND 
	// ISSUE: AXIS IS WEIRD
	// ISSUE: HOVER OVER PREVIEW?
	// ISSUE: HOVER OVER CSS STYLING

	// set main plot window to [t_max-90days,t_max] by default
	Note.plotOptions.xaxis.min = minDate;
	Note.plotOptions.xaxis.max = maxDate;
	Note.plotOptions.xaxis.panRange = [minDate, maxDate];
	Note.plotOptions.xaxis.zoomRange = [50000, maxDate - minDate]

	// set nav plot window to [t_min, t_max] permanently
	Note.navOptions.xaxis.min = minDate;
	Note.navOptions.xaxis.max = maxDate;
	Note.navOptions.xaxis.panRange = [minDate, maxDate];

	// mark hospital stays
	for (var i = hospitalStays.length - 1; i >= 0; i--) {
		Note.plotOptions.grid.markings.push({ xaxis: { from: hospitalStays[i][0], to: hospitalStays[i][1]} });
	}

	// plot dataseries
	 var note_plot = $.plot("#note_plot_target", Note.plotData, Note.plotOptions);
	 console.log("note plot is " + Note.plotOptions.xaxis.panRange);
	 var note_nav = $.plot("#note_nav_target", Note.plotData, Note.navOptions);
	 console.log("note plot is " + Note.navOptions.xaxis.panRange);

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

        // set tooltip contents
        set_preview_data(item.series.label,item.dataIndex)

        // $("#tooltip").html("<strong>Percentile:</strong> " + y + "<br><strong> Dose: </strong> " + x + " Gy")
        $("#note_tooltip").html(Note.curr_timestamp + "<br><strong> Type: </strong> " + Note.curr_type + "<br><strong> \
        	Service: </strong> " + Note.curr_service + "<br><strong> Preview: </strong>" + Note.curr_preview)
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


	function replot(ranges){
		if (ranges.xaxis.from != ranges.xaxis.to){
			var axis = note_plot.getAxes().xaxis;
			var opts = axis.options;
			opts.min = ranges.xaxis.from;
			opts.max = ranges.xaxis.to;
			note_plot.setupGrid();
			note_plot.draw();
			note_plot.clearSelection();
		}
	}
	// now connect the two

	$("#note_nav_target").bind("plotselected", function (event, ranges) {
		note_plot.setSelection(ranges);
	});

	$("#note_plot_target").bind("plotpan", function (event, plot) {
		var axes = note_plot.getAxes();
		var ranges = { xaxis: { from: axes.xaxis.min, to: axes.xaxis.max }, yaxis: { from: axes.yaxis.min, to: axes.yaxis.max } }
		note_nav.setSelection(ranges, true);
	});

	$("#note_plot_target").bind("plotzoom", function (event, plot) {
		var axes = note_plot.getAxes();
		var ranges = { xaxis: { from: axes.xaxis.min, to: axes.xaxis.max }, yaxis: { from: axes.yaxis.min, to: axes.yaxis.max } }
		note_nav.setSelection(ranges, true);
	});

	$("#note_nav_target").bind("plotshift", function (event, plot) {
		newrange = note_nav.getNewSelection();
		note_nav.setSelection(newrange, true);
		replot(newrange);
	});

}


function displayToast(content){
	var noteToast = document.getElementById('note_detail');
	noteToast.toggle();
	noteToast.innerHTML = content;
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


function set_preview_data(service,idx){
	Note.curr_preview = notePreviews[service][idx]['preview'];
	console.log(Note.curr_preview);
	Note.curr_service = notePreviews[service][idx]['service'];
	Note.curr_type = notePreviews[service][idx]['type'];
	Note.curr_timestamp = notePreviews[service][idx]['time'];
	Note.curr_noteID = notePreviews[service][idx]['id'];
}

function get_fulltext(service,idx){
	var text;
	$.getJSON( "/_note/" + service + "/" + idx + "/" , function(result) {
		console.log(result);
		text= result.fulltext;
	});
	return text;
}