

var Note = {};
Note.base = 1;
Note.step = 0.2;
Note.curr_preview = "";
Note.curr_type = "";
Note.curr_service = "";
Note.curr_timestamp = "";
Note.curr_fulltext = "";
Note.curr_noteID = 0;

function plotNoteTimeline(noteSeries, hospitalStays, minDate, maxDate){

	// for now...
	return

	// plot dataseries
	// attach event listeners?

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
    $("#note_placeholder").bind("plothover", function (event, pos, item) {
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
	$("#note-placeholder").mouseleave(function(){
		$("#note_tooltip").hide();     
	});


}

function createNoteTimeline(noteDataArray, minDate) {
	console.log(minDate);
	var items = new vis.DataSet(noteDataArray);
	var maxDate = new Date();
	
	var groups = new vis.DataSet([
		{id: 1, content: 'Notes', value: 1},
		{id: 2, content: 'Consults', value: 2},
		{id: 3, content: 'Radiology Reports', value: 3},
		{id: 4, content: 'Nursing Notes', value: 4}
	]);

	// create visualization
	var container = document.getElementById('note_visualization');
	var options = {
		min: minDate,             // lower limit of visible range
	    max: maxDate,                // upper limit of visible range
	    zoomMin: 7 * 1000 * 60 * 60 * 24,             // one week in milliseconds
	    zoomMax: 365 * 1000 * 60 * 60 * 24 * 31 * 3,    // about three years in milliseconds
	
	// option groupOrder can be a property name or a sort function
	// the sort function must compare two groups and return a value
	//     > 0 when a > b
	//     < 0 when a < b
	//       0 when a == b
		groupOrder: function (a, b) {
		  return a.value - b.value;
		},
		editable: false,
		type: 'point'
	};

	note_timeline = new vis.Timeline(container);
	note_timeline.setOptions(options);
	note_timeline.setGroups(groups);
	note_timeline.setItems(items);
	note_timeline.setWindow(minDate,maxDate);

	/**
     * When the note_timeline selects an object (or multiple objects), add object(s) 
     * as defined in properties to the chart below
     */
	note_timeline.on('select', function (properties) {
      console.log("adding- " + JSON.stringify(properties))
    });

    /**
     * When the note_timeline range is changed, trigger the chart to readjust the 
     * range according to the time range defined in properties
     */
	note_timeline.on('rangechanged', function (properties) {
      console.log("changing range- " + JSON.stringify(properties));
    });
}


function addNoteEventListeners() {
	// attach events to the navigation buttons
    document.getElementById('note_zoomIn').onclick    = function () { note_zoom(-0.2); };
    document.getElementById('note_zoomOut').onclick   = function () { note_zoom( 0.2); };
    document.getElementById('note_moveLeft').onclick  = function () { note_move( 0.2); };
    document.getElementById('note_moveRight').onclick = function () { note_move(-0.2); };


    var note_selection = document.getElementById('note_selection');
	var note_select = document.getElementById('note_select');
	var note_focus = document.getElementById('note_focus');

	note_select.onclick = function () {
		var ids = note_selection.value.split(',').map(function (value) {
		  return value.trim();
		});
		note_timeline.setSelection(ids, {focus: "checked"});
	};
}


function getToast(note_index){
	$.getJSON( "/_note/" + note_index, function(result) {
		console.log(result);
		var text= result.fulltext;
		var title ="note";
		Command: toastr["info"](text, title.toUpperCase())

		toastr.options = {
		  "closeButton": true,
		  "debug": false,
		  "newestOnTop": true,
		  "progressBar": false,
		  "positionClass": "toast-top-full-width",
		  "preventDuplicates": false,
		  "showDuration": "3000",
		  "hideDuration": "1000",
		  "timeOut": "50000",
		  "extendedTimeOut": "1000",
		  "showEasing": "swing",
		  "hideEasing": "linear",
		  "showMethod": "fadeIn",
		  "hideMethod": "fadeOut"
		}
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




/**
 * Move the timeline a given percentage to left or right
 * @param {Number} percentage   For example 0.1 (left) or -0.1 (right)
 */
function note_move (percentage) {
    var range = note_timeline.getWindow();
    var interval = range.end - range.start;

    note_timeline.setWindow({
        start: range.start.valueOf() - interval * percentage,
        end:   range.end.valueOf()   - interval * percentage
    });


    med_timeline.setWindow({
        start: range.start.valueOf() - interval * percentage,
        end:   range.end.valueOf()   - interval * percentage
    });
}

/**
 * Zoom the timeline a given percentage in or out
 * @param {Number} percentage   For example 0.1 (zoom out) or -0.1 (zoom in)
 */
function note_zoom (percentage) {
    var range = note_timeline.getWindow();
    var interval = range.end - range.start;

    note_timeline.setWindow({
        start: range.start.valueOf() - interval * percentage,
        end:   range.end.valueOf()   + interval * percentage
    });


    med_timeline.setWindow({
        start: range.start.valueOf() - interval * percentage,
        end:   range.end.valueOf()   + interval * percentage
    });

}
