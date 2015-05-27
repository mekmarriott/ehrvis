
var note_plot, note_nav;
var Note = {};
Note.day = 24*60*60*1000;
Note.base = 1;
Note.step = 0.2;
Note.padding = 0.3;
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
Note.plotOptions.series = { lines: {show: false}, points: {show: true, radius: 4.5 }};
Note.plotOptions.grid = { hoverable: true, clickable: true, markings: [] };
Note.plotOptions.yaxis = { min: 1-Note.padding, autoscaleMargin: Note.padding, zoomRange: false, ticks: [], panRange: false }; 
Note.plotOptions.xaxis = { mode: "time", zoomRange: [21*Note.day,365*Note.day], panRange: [0,1] };
Note.plotOptions.zoom = { interactive: true };
Note.plotOptions.pan = { interactive: true }; 


// plotting options for navigation strip

Note.navOptions = {};
Note.navOptions.series = { lines: {show: false}, points: {show: true }};
Note.navOptions.grid = { hoverable: true, clickable: true, markings: [] };
Note.navOptions.yaxis = { min: 1-Note.padding/2, autoscaleMargin: Note.padding/2, ticks: [], panRange: false }; 
Note.navOptions.xaxis = { mode: "time", panRange: [0,1] , tickSize: [3, "month"] };
Note.navOptions.shift = { interactive: true };
Note.navOptions.legend = { show: false };
Note.navOptions.selection =  { mode: null, color: "#88baee" }

function createNoteTimeline(noteSeries, hospitalStays, minDate, maxDate){

	// assign dataseries:
	Note.plotData = noteSeries;
	
	// convert heighcounts to heights
	for (var i = Note.plotData.length - 1; i >= 0; i--) {
		height_conversion(Note.plotData[i].data)
	};

	// TODO: SEARCH/FILTER POINTS?
	// TODO: CSS - PLOT CONTAINER/WINDOW ADAPTATION

	// set main plot window to [t_max-90days,t_max] by default
	Note.plotOptions.xaxis.min = minDate;//maxDate - 90*(24*60*60*1000);
	Note.plotOptions.xaxis.max = maxDate;
	Note.plotOptions.xaxis.panRange = [minDate, maxDate];

	// set nav plot window to [t_min, t_max] permanently
	Note.navOptions.xaxis.min = minDate;
	Note.navOptions.xaxis.max = maxDate;
	Note.navOptions.xaxis.panRange = [minDate, maxDate];

	// mark hospital stays
	for (var i = hospitalStays.length - 1; i >= 0; i--) {
		Note.plotOptions.grid.markings.push({ xaxis: { from: hospitalStays[i][0], to: hospitalStays[i][1]}, color: "#e5e7e5" });
		Note.navOptions.grid.markings.push({ xaxis: { from: hospitalStays[i][0], to: hospitalStays[i][1]}, color: "#e5e7e5" });
	}

	// plot dataseries
	var note_plot = $.plot("#note_plot_target", Note.plotData, Note.plotOptions);
	var note_nav = $.plot("#note_nav_target", Note.plotData, Note.navOptions);

	$("#note_plot_target div.legend table").css({ "font-size": "1.8rem", "background-color":"#d5d5d5", color:"#222", "opacity":0.85, padding:"0.5rem", border:"1rem" });

	// set initial range
	var axes = note_plot.getAxes();
	var initRange = { xaxis: { from: maxDate - 90*(24*60*60*1000), to: maxDate }, yaxis: { from: axes.yaxis.min, to: axes.yaxis.max } }
	note_nav.setSelection(initRange, true);
	replot(initRange);

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


    //Bind "fulltext on click" to plot
    $("#note_plot_target").bind("plotclick", function (event, pos, item) {
    	note_plot.unhighlight()
      if (item) {
        set_fulltext(item.series.label,item.dataIndex);
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
		note_plot.highlight(item.series, item.dataIndex);
      }
    });

    //Bind tooltip to plot
    $("#note_plot_target").bind("plothover", function (event, pos, item) {
      if (item) {

        // set tooltip contents
        set_preview_data(item.series.label,item.dataIndex)

   
        // $("#tooltip").html("<strong>Percentile:</strong> " + y + "<br><strong> Dose: </strong> " + x + " Gy")
        $("#note_tooltip").html(Note.curr_timestamp + "<br><strong> Type: </strong> " + Note.curr_type + "<br><strong> \
        	Service: </strong> " + Note.curr_service + "<br><strong> Preview: </strong>" + Note.curr_preview)
          .css({top: item.pageY+5, left: item.pageX+5, 'background-color':item.series.color})
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


function displayFulltext(){
	var noteToast = document.getElementById('note_detail');
	noteToast.toggle();
	console.log(Note.curr_fulltext);
	noteToast.innerHTML = lipsum;
	// noteToast.innerHTML = Note.curr_fulltext;
	noteToast.heading = Note.curr_type;
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

function set_fulltext(service,idx){
	$.getJSON( "/_note/" + service + "/" + idx + "/fulltext" , function(result) {
		Note.curr_fulltext= result.fulltext;
		displayFulltext();
	});
}

var lipsum = "<p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Donec a diam lectus. Sed sit amet ipsum mauris. Maecenas congue ligula ac quam viverra nec consectetur ante hendrerit. Donec et mollis dolor. Praesent et diam eget libero egestas mattis sit amet vitae augue. Nam tincidunt congue enim, ut porta lorem lacinia consectetur. Donec ut libero sed arcu vehicula ultricies a non tortor. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Aenean ut gravida lorem. Ut turpis felis, pulvinar a semper sed, adipiscing id dolor. Pellentesque auctor nisi id magna consequat sagittis. Curabitur dapibus enim sit amet elit pharetra tincidunt feugiat nisl imperdiet. Ut convallis libero in urna ultrices accumsan. Donec sed odio eros. Donec viverra mi quis quam pulvinar at malesuada arcu rhoncus. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. In rutrum accumsan ultricies. Mauris vitae nisi at sem facilisis semper ac in est.</p><br><p>Vivamus fermentum semper porta. Nunc diam velit, adipiscing ut tristique vitae, sagittis vel odio. Maecenas convallis ullamcorper ultricies. Curabitur ornare, ligula semper consectetur sagittis, nisi diam iaculis velit, id fringilla sem nunc vel mi. Nam dictum, odio nec pretium volutpat, arcu ante placerat erat, non tristique elit urna et turpis. Quisque mi metus, ornare sit amet fermentum et, tincidunt et orci. Fusce eget orci a orci congue vestibulum. Ut dolor diam, elementum et vestibulum eu, porttitor vel elit. Curabitur venenatis pulvinar tellus gravida ornare. Sed et erat faucibus nunc euismod ultricies ut id justo. Nullam cursus suscipit nisi, et ultrices justo sodales nec. Fusce venenatis facilisis lectus ac semper. Aliquam at massa ipsum. Quisque bibendum purus convallis nulla ultrices ultricies. Nullam aliquam, mi eu aliquam tincidunt, purus velit laoreet tortor, viverra pretium nisi quam vitae mi. Fusce vel volutpat elit. Nam sagittis nisi dui.</p><br><p>Suspendisse lectus leo, consectetur in tempor sit amet, placerat quis neque. Etiam luctus porttitor lorem, sed suscipit est rutrum non. Curabitur lobortis nisl a enim congue semper. Aenean commodo ultrices imperdiet. Vestibulum ut justo vel sapien venenatis tincidunt. Phasellus eget dolor sit amet ipsum dapibus condimentum vitae quis lectus. Aliquam ut massa in turpis dapibus convallis. Praesent elit lacus, vestibulum at malesuada et, ornare et est. Ut augue nunc, sodales ut euismod non, adipiscing vitae orci. Mauris ut placerat justo. Mauris in ultricies enim. Quisque nec est eleifend nulla ultrices egestas quis ut quam. Donec sollicitudin lectus a mauris pulvinar id aliquam urna cursus. Cras quis ligula sem, vel elementum mi. Phasellus non ullamcorper urna.\</p><br><p>Class aptent taciti sociosqu ad litora torquent per conubia nostra, per inceptos himenaeos. In euismod ultrices facilisis. Vestibulum porta sapien adipiscing augue congue id pretium lectus molestie. Proin quis dictum nisl. Morbi id quam sapien, sed vestibulum sem. Duis elementum rutrum mauris sed convallis. Proin vestibulum magna mi. Aenean tristique hendrerit magna, ac facilisis nulla hendrerit ut. Sed non tortor sodales quam auctor elementum. Donec hendrerit nunc eget elit pharetra pulvinar. Suspendisse id tempus tortor. Aenean luctus, elit commodo laoreet commodo, justo nisi consequat massa, sed vulputate quam urna quis eros. Donec vel.</p>"
