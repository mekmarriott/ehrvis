function loadMedicationData(){
	$.getJSON( "/_medications/", function(result) {
		medEvents = result['medication_data'];
		minDate = result['minDate'];
		med_display_indices = result['med_indices']
		med_display_names = result['med_names']
		var medDataArray = [];
		for (var i in medEvents){
			var medEvent = {
				id: i,
				group: medEvents[i].display_group,
				content: '<a href="#" title="' + medEvents[i].name + '">' + medEvents[i].name + '</a>',
				// title = "put text for tooltip here", what goes between > < is what you want shown on the timeline
				start: medEvents[i].start,
				end: medEvents[i].end,
				//subgroup: <- fill in subgroup
			}
			medDataArray.push(medEvent);
		}
		createMedicationTimeline(medDataArray, minDate);
	});
}

function createMedicationTimeline(medDataArray, minDate) {
	var items = new vis.DataSet(medDataArray);
	var maxDate = new Date();


	var visGroups = [];
	for (var i = med_display_indices.length - 1; i >= 0; i--) {
		 visGroups.push( {id: med_display_indices[i], content: med_display_names[i], value: i} );
	};


	var groups = new vis.DataSet(visGroups);

	// create visualization
	var container = document.getElementById('med_visualization');
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
		margin: {
	      item: 20,
	      axis: 40
	    }
	};

	med_timeline = new vis.Timeline(container);
	med_timeline.setOptions(options);
	med_timeline.setGroups(groups);
	med_timeline.setItems(items);
	med_timeline.setWindow(minDate,maxDate);


	/**
     * When the med_timeline selects an object (or multiple objects), add object(s) 
     * as defined in properties to the chart below
     */
	med_timeline.on('select', function (properties) {
      console.log("adding- " + JSON.stringify(properties))
    });

    /**
     * When the med_timeline range is changed, trigger the chart to readjust the 
     * range according to the time range defined in properties
     */
	med_timeline.on('rangechanged', function (properties) {
      console.log("changing range- " + JSON.stringify(properties));
    });
}

function addMedEventListeners() {
	// attach events to the navigation buttons
    document.getElementById('med_zoomIn').onclick    = function () { med_zoom(-0.2); };
    document.getElementById('med_zoomOut').onclick   = function () { med_zoom( 0.2); };
    document.getElementById('med_moveLeft').onclick  = function () { med_move( 0.2); };
    document.getElementById('med_moveRight').onclick = function () { med_move(-0.2); };

    /**
     *Select + move window dynamically to view selections
    */
    var med_selection = document.getElementById('med_selection');
	var med_select = document.getElementById('med_select');
	var med_focus = document.getElementById('med_focus');

	med_select.onclick = function () {
		var ids = med_selection.value.split(',').map(function (value) {
		  return value.trim();
		});
		med_timeline.setSelection(ids, {focus: "checked"});
	};
}

	/**
     * Move the timeline a given percentage to left or right
     * @param {Number} percentage   For example 0.1 (left) or -0.1 (right)
     */
    function med_move (percentage) {
        var range = note_timeline.getWindow();
        var interval = range.end - range.start;

        med_timeline.setWindow({
            start: range.start.valueOf() - interval * percentage,
            end:   range.end.valueOf()   - interval * percentage
        });
	}

    /**
     * Zoom the timeline a given percentage in or out
     * @param {Number} percentage   For example 0.1 (zoom out) or -0.1 (zoom in)
     */
    function med_zoom (percentage) {
        var range = note_timeline.getWindow();
        var interval = range.end - range.start;

        med_timeline.setWindow({
            start: range.start.valueOf() - interval * percentage,
            end:   range.end.valueOf()   + interval * percentage
        });
    }
