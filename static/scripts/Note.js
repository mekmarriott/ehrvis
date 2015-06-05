// Author: Baris Ungun, Emma Marriott (both authors contributed significantly to most portions; sections are marked below with lead author indicated)
// Description: This script defines the note timeline library
// Dependencies: flot.js, jQuery



// < NOTE OBJECT: SETUP FOR DATA PLOTTING; SET UP FOR PREVIEW AND FULL TEXT DISPLAY HANDLING --- Lead : BU >

var note_plot, note_nav;
var Note = {};

// 1 day in milliseconds
Note.day = 24*60*60*1000;

// plotting constants
Note.base = 1;
Note.step = 0.2;
Note.padding = 0.3;

// placeholders for preview and full text information
Note.curr_preview = "";
Note.curr_type = "";
Note.curr_service = "";
Note.curr_timestamp = "";
Note.curr_fulltext = "";
Note.curr_noteID = 0;

// background color for hospitalization periods
Note.inpatientColor = "#e0e5e1"


// data format: [ { data: ---, label: ---}, {data: ----, label: ---}, ... ]
Note.plotData = [];


// default plotting options for main timeline
Note.plot_min = 0;
Note.plot_max = 1;
Note.plotOptions = {};
Note.plotOptions.series = { lines: {show: false}, points: {show: true, radius: 4.5 }};

// enable hovering and clicking for mouse-over previews and full text pop-up on click
Note.plotOptions.grid = { hoverable: true, clickable: true, markings: [] };


// disable y zooming and panning; disable tick marks, 
Note.plotOptions.yaxis = { min: 1-Note.padding, autoscaleMargin: Note.padding, zoomRange: false, ticks: [], panRange: false }; 

// zoomRange - min x range: 21 days , max x range: 365 days
// panRange - placeholder
Note.plotOptions.xaxis = { mode: "time", zoomRange: [21*Note.day,365*Note.day], panRange: [0,1] };

// enable zooming and panning
Note.plotOptions.zoom = { interactive: true };
Note.plotOptions.pan = { interactive: true }; 


// default plotting options for navigation strip
Note.navOptions = {};
Note.navOptions.series = { lines: {show: false}, points: {show: true }};
Note.navOptions.grid = { hoverable: true, clickable: true, markings: [] };
Note.navOptions.yaxis = { min: 1-Note.padding/2, autoscaleMargin: Note.padding/2, ticks: [], panRange: false }; 
Note.navOptions.xaxis = { mode: "time", panRange: [0,1] , tickSize: [3, "month"] };

// enable shift ( nav plot drives main plot )
Note.navOptions.shift = { interactive: true };
Note.navOptions.legend = { show: false };
Note.navOptions.selection =  { mode: null, color: "#88baee" }


// given an array of javascript objects (with fields label,data,color,symbol) reformat slightly to conform to flot.js' expected structure
//  handle formatting including series color and series marker shape ("symbol") 
Note.formSeries= function(series){
	out = [];
	for (var i = series.length - 1; i >= 0; i--) {
		out.push({label: series[i].label, data: series[i].data, color: series[i].color, points: {show: true, symbol: series[i].symbol}, lines: {show: false } })
	};
	return out
}


// *** primary call from [name].html ***
// -performs plotting using flot.js library (jQuery dependent)
// -binds event listeners to plot
// -requires the existence of <div>s with div-id's "note_plot_target" and "note_nav_target" & validly specified heights (flot.js requirement)
// 		for proper function
// -explicit inputs: 
//			1. noteSeries: data array to be parsed by method Note.formSeries, see above;
//			2. hospitalStays: data array containing a series of data points: first and last day of each hospitalization as a length 2 array);
//			3. minDate, maxDate: earliest and latest dates in the patient record; maximum temporal scope to be displayed in timelines.
Note.createNoteTimeline = function(noteSeries, hospitalStays, minDate, maxDate){

	// < BASIC DATA PLOTTING --- Lead : BU >

	// assign dataseries:
	Note.plotData = Note.formSeries(noteSeries);


	// convert heighcounts to heights
	for (var i = Note.plotData.length - 1; i >= 0; i--) {
		Note.heightConversion(Note.plotData[i].data)
	};


	// set main plot window to [t_max-90days,t_max] by default
	Note.plotOptions.xaxis.min = Math.max(minDate,maxDate - 90*(24*60*60*1000))
	Note.plotOptions.xaxis.max = maxDate;
	Note.plotOptions.xaxis.panRange = [minDate, maxDate];

	// set nav plot window to [t_min, t_max] permanently
	Note.navOptions.xaxis.min = minDate;
	Note.navOptions.xaxis.max = maxDate;
	Note.navOptions.xaxis.panRange = [minDate, maxDate];

	// mark hospital stays
	for (var i = hospitalStays.length - 1; i >= 0; i--) {
		Note.plotOptions.grid.markings.push({ xaxis: { from: hospitalStays[i][0], to: hospitalStays[i][1]}, color: Note.inpatientColor });
		Note.navOptions.grid.markings.push({ xaxis: { from: hospitalStays[i][0], to: hospitalStays[i][1]}, color: Note.inpatientColor });
	}

	// plot dataseries
	var note_plot = $.plot("#note_plot_target", Note.plotData, Note.plotOptions);
	var note_nav = $.plot("#note_nav_target", Note.plotData, Note.navOptions);

	$("#note_plot_target div.legend table").css({ "font-size": "1.8rem", "background-color":"#d5d5d5", color:"#222", "opacity":0.85, padding:"0.5rem", border:"1rem" });

	// highlight initial viewing range (for main plot) as selection region in nav plot
	var axes = note_plot.getAxes();
	var initRange = { xaxis: { from: Math.max(minDate,maxDate - 90*(24*60*60*1000)), to: maxDate }, yaxis: { from: axes.yaxis.min, to: axes.yaxis.max } }
	note_nav.setSelection(initRange, true);
	replot(initRange);


	// < PLOT MANIPULATION & SYNCHRONIZATION --- Lead : EM >


    //Bind "fulltext on click" to plot
    $("#note_plot_target").bind("plotclick", function (event, pos, item) {
    	note_plot.unhighlight()
      if (item) {
        Note.setFulltext(item.series.label,item.dataIndex);
      } 
    });

    $("#note_nav_target").bind("plotclick", function (event, pos, item) {
    	note_plot.unhighlight()
      if (item) {
      	var centerPoint = item.datapoint[0];
      	var axes = note_plot.getAxes();
		var diff = axes.xaxis.max - axes.xaxis.min;
		var ranges = { xaxis: { from: centerPoint - diff*0.5, to: centerPoint + diff*0.5 }, yaxis: { from: axes.yaxis.min, to: axes.yaxis.max } }
        note_nav.setSelection(ranges, true);
		replot(ranges);
		// note_plot.highlight(item.series, item.dataIndex);
      }
    });


	// < TOOLTIP FUNCTIONS --- Lead : BU >

	// create tooltip div 
	$("<div id='note_tooltip'></div>").css({
		position: "absolute",
		display: "none",
		border: "1px solid #fdd",
		padding: "5px",
		"background-color": "#f00",
		color: "#ddd",
		opacity: 0.9,
		"border-radius": "5px",
		"font-size": "1.5rem"
	}).appendTo("body");


    //Bind tooltip to plot
    $("#note_plot_target").bind("plothover", function (event, pos, item) {
      if (item) {

        // set tooltip contents based on the point selected---identified by which data series the point belongs to and its position within the
        // 	sequence of points in the data series.
        Note.setPreviewData(item.series.label,item.dataIndex)
   
        // handle cases when selected point close to right edge of page:
        var dist_to_edge = window.innerWidth - item.pageX, ttip_pos = item.pageX+5;

        // add leftward offset to keep tooltip from running over to right
        if (dist_to_edge < 250){
        	ttip_pos -= (250-dist_to_edge);
        }


        // Populate inner html of tooltip with preview data about selected note (as stored in object Note); 
        // modify css styling of tooltip to track position of selected point
        $("#note_tooltip").html(Note.curr_timestamp + "<br><strong> Type: </strong> " + Note.curr_type + "<br><strong> \
        	Service: </strong> " + Note.curr_service + "<br><strong> Preview: </strong>" + Note.curr_preview)
          .css({top: item.pageY+5, left: ttip_pos, 'background-color':item.series.color})
          .fadeIn(200);
      } else {
        $("#note_tooltip").hide();
      }
    });


	//Hide tooltip div when mouse leaves note plot panel
	$("#note_plot_target").mouseleave(function(){
		$("#note_tooltip").hide();     
	});


	// < NAVIGATION FUNCTIONS --- Lead : EM >

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


	// < FILTERING FUNCTIONS --- Lead : EM >


	// button selecting/filtering controls
	var choiceContainer = $("#choices");
	choiceContainer.append("<strong style='margin-top: 11px; border-radius: 20px; margin-right: 5px;'> Filter Options: </strong>");
	for (var i = Note.plotData.length - 1; i >= 0; i--) {
		var checkhtml = "<button class='btn btn-default choice-button pressed' name='" + i + "' style='margin: 5px; color: white; background: " + 
						Note.plotData[i].color + "'>" + Note.plotData[i].label + " </button>"
		choiceContainer.append(checkhtml);
	};

	$("#choices button").click(function() {
		console.log("clicked");
	    $(this).toggleClass('pressed').promise().done(function(){
	    	plotAccordingToChoices();
	    });
	});

	function plotAccordingToChoices() {
		$("#choices").find('button').each(function(index) {
    		var idx = $(this).attr('name');
			if ($(this).hasClass("pressed")) {
				Note.plotData[idx].points.show = true
				console.log(idx + "is pressed")
			} else {
				Note.plotData[idx].points.show = false
				console.log(idx + "is not pressed")
			}
			var axes = note_plot.getAxes();
			Note.plotOptions.xaxis.min = axes.xaxis.min
			Note.plotOptions.xaxis.max = axes.xaxis.max
			note_plot = $.plot("#note_plot_target", Note.plotData, Note.plotOptions);
		});

	}

	$("#note_plot_target").append("<div id='inpatientkey' style='position:absolute;left:30px;top:20px;color:#666;font-size:small; box-shadow:0.2rem 0.2rem #000'></div>")
	$("#inpatientkey").append("<div id='ik-inner' style='width: 150px; height: 25px; background-color:"+Note.inpatientColor+"; padding-top:0.5rem; text-align:center'>Inpatient Periods</div>")
	$("#inpatientkey").append("<div id='ik-inner' style='width: 150px; height: 25px; background-color:#fff; padding-top:0.5rem; text-align:center'>Outpatient Periods</div>")

	// $(Inpatient stays <div style='background-color:red'></div>");
	// $("#note_plot_target").append("<div style='position:absolute;left:30px;top:40px;color:#666;font-size:small'>Outpatient <div style='background-color:red'></div></div>");

}


// auxiliary functions, intended primarily for internal calls 


// when called, displays pop-up window with full text of the note corresponding to the most recently selected data point
// ( or, more precisely, displays the contents of the variable Note.curr_fulltext )
Note.displayFulltext = function(){
	var noteToast = document.getElementById('note_detail');

	// display pop-up
	noteToast.toggle();

	// set pop-up text content to be full text of note
	// noteToast.innerHTML = lipsum;
	noteToast.innerHTML = Note.curr_fulltext;

	// set pop-up header to be type of note (e.g., Progress Note, Discharge Summary)
	noteToast.heading = Note.curr_type;
}


// < PLOTTING UTILIES --- Lead : BU >

// convert count (Nth note per day) to y-value for plotting
Note.count2Height= function(count){
	return Note.base + Note.step*(count-1);
}


// convert count (Nth note per day) to y-value for plotting
Note.heightConversion = function(data_array){
	// data array expected to be in form [ [ date_1, count_1] , [date_2,count_2] , ... ]
	for (var i = data_array.length - 1; i >= 0; i--) {

		// for ith [date,count] pair, get second value (index 1), convert count to height
		data_array[i][1]=Note.count2Height(data_array[i][1]);
	};
}


// store information---to be displayed in hover-over preview of note---in relevant fields of object Note.
// retrieve note preview data from container object notePreviews based on service (i.e., data series) and index (i.e., point # idx in said data series)
Note.setPreviewData = function(service,idx){
	// preview text
	Note.curr_preview = notePreviews[service][idx]['preview'];
	// name of service
	Note.curr_service = notePreviews[service][idx]['service'];
	// note type
	Note.curr_type = notePreviews[service][idx]['type'];
	// note timestamp
	Note.curr_timestamp = notePreviews[service][idx]['time'];
	// unique ID
	Note.curr_noteID = notePreviews[service][idx]['id'];
}

// store information---to be displayed in pop-up dialog box for full text of note---in relevant field of object Note
Note.setFulltext = function(service,idx){
	// retrieve note full text data from server
	$.getJSON( "/_note/" + service + "/" + idx + "/fulltext/" , function(result) {
		Note.curr_fulltext= result.fulltext;
		Note.displayFulltext();
	});
}


// filler text to demonstrate scrolling functionality in dialog box displaying note fulltext
var lipsum = "<p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Donec a diam lectus. Sed sit amet ipsum mauris. Maecenas congue ligula ac quam viverra nec consectetur ante hendrerit. Donec et mollis dolor. Praesent et diam eget libero egestas mattis sit amet vitae augue. Nam tincidunt congue enim, ut porta lorem lacinia consectetur. Donec ut libero sed arcu vehicula ultricies a non tortor. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Aenean ut gravida lorem. Ut turpis felis, pulvinar a semper sed, adipiscing id dolor. Pellentesque auctor nisi id magna consequat sagittis. Curabitur dapibus enim sit amet elit pharetra tincidunt feugiat nisl imperdiet. Ut convallis libero in urna ultrices accumsan. Donec sed odio eros. Donec viverra mi quis quam pulvinar at malesuada arcu rhoncus. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. In rutrum accumsan ultricies. Mauris vitae nisi at sem facilisis semper ac in est.</p><br><p>Vivamus fermentum semper porta. Nunc diam velit, adipiscing ut tristique vitae, sagittis vel odio. Maecenas convallis ullamcorper ultricies. Curabitur ornare, ligula semper consectetur sagittis, nisi diam iaculis velit, id fringilla sem nunc vel mi. Nam dictum, odio nec pretium volutpat, arcu ante placerat erat, non tristique elit urna et turpis. Quisque mi metus, ornare sit amet fermentum et, tincidunt et orci. Fusce eget orci a orci congue vestibulum. Ut dolor diam, elementum et vestibulum eu, porttitor vel elit. Curabitur venenatis pulvinar tellus gravida ornare. Sed et erat faucibus nunc euismod ultricies ut id justo. Nullam cursus suscipit nisi, et ultrices justo sodales nec. Fusce venenatis facilisis lectus ac semper. Aliquam at massa ipsum. Quisque bibendum purus convallis nulla ultrices ultricies. Nullam aliquam, mi eu aliquam tincidunt, purus velit laoreet tortor, viverra pretium nisi quam vitae mi. Fusce vel volutpat elit. Nam sagittis nisi dui.</p><br><p>Suspendisse lectus leo, consectetur in tempor sit amet, placerat quis neque. Etiam luctus porttitor lorem, sed suscipit est rutrum non. Curabitur lobortis nisl a enim congue semper. Aenean commodo ultrices imperdiet. Vestibulum ut justo vel sapien venenatis tincidunt. Phasellus eget dolor sit amet ipsum dapibus condimentum vitae quis lectus. Aliquam ut massa in turpis dapibus convallis. Praesent elit lacus, vestibulum at malesuada et, ornare et est. Ut augue nunc, sodales ut euismod non, adipiscing vitae orci. Mauris ut placerat justo. Mauris in ultricies enim. Quisque nec est eleifend nulla ultrices egestas quis ut quam. Donec sollicitudin lectus a mauris pulvinar id aliquam urna cursus. Cras quis ligula sem, vel elementum mi. Phasellus non ullamcorper urna.\</p><br><p>Class aptent taciti sociosqu ad litora torquent per conubia nostra, per inceptos himenaeos. In euismod ultrices facilisis. Vestibulum porta sapien adipiscing augue congue id pretium lectus molestie. Proin quis dictum nisl. Morbi id quam sapien, sed vestibulum sem. Duis elementum rutrum mauris sed convallis. Proin vestibulum magna mi. Aenean tristique hendrerit magna, ac facilisis nulla hendrerit ut. Sed non tortor sodales quam auctor elementum. Donec hendrerit nunc eget elit pharetra pulvinar. Suspendisse id tempus tortor. Aenean luctus, elit commodo laoreet commodo, justo nisi consequat massa, sed vulputate quam urna quis eros. Donec vel.</p>"
