function createNoteTimeline(noteDataArray, minDate) {
	console.log(minDate);
	var items = new vis.DataSet(noteDataArray);
	
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
	    max: new Date(),                // upper limit of visible range
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
		editable: false
	};

	note_timeline = new vis.Timeline(container);
	note_timeline.setOptions(options);
	note_timeline.setGroups(groups);
	note_timeline.setItems(items);

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