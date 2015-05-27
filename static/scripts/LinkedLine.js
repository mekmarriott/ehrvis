$(function() {

		var d = [[119.6463600000, 0], [119.6550000000, 0], [119.6636400000, 0], [119.6722800000, 77], [119.6809200000, 3636], [119.6895600000, 3575], [119.6982000000, 2736], [119.7068400000, 1086], [119.7154800000, 676], [119.7241200000, 1205], [119.7327600000, 906], [119.7414000000, 710], [119.7500400000, 639], [119.7586800000, 540], [119.7673200000, 435], [119.7759600000, 301], [119.7846000000, 575], [119.7932400000, 481], [119.8018800000, 591], [119.8105200000, 608], [119.8191600000, 459], [119.8278000000, 234], [119.8364400000, 1352], [119.8450800000, 686], [119.8537200000, 279], [119.8623600000, 449], [119.8710000000, 468], [119.8796400000, 392], [119.8882800000, 282], [119.8969200000, 208], [119.9055600000, 229], [119.9142000000, 177], [119.9228400000, 374], [119.9314800000, 436], [119.9401200000, 404], [119.9487600000, 253], [119.9574000000, 218], [119.9660400000, 476], [119.9746800000, 462], [119.9833200000, 448], [119.9919600000, 442], [120.0006000000, 403], [120.0092400000, 204], [120.0178800000, 194], [120.0265200000, 327], [120.0351600000, 374], [120.0438000000, 507], [120.0524400000, 546], [120.0610800000, 482], [120.0697200000, 283], [120.0783600000, 221], [120.0870000000, 483], [120.0956400000, 523], [120.1042800000, 528], [120.1129200000, 483], [120.1215600000, 452], [120.1302000000, 270], [120.1388400000, 222], [120.1474800000, 439], [120.1561200000, 559], [120.1647600000, 521], [120.1734000000, 477], [120.1820400000, 442], [120.1906800000, 252], [120.1993200000, 236], [120.2079600000, 525], [120.2166000000, 477], [120.2252400000, 386], [120.2338800000, 409], [120.2425200000, 408], [120.2511600000, 237], [120.2598000000, 193], [120.2684400000, 357], [120.2770800000, 414], [120.2857200000, 393], [120.2943600000, 353], [120.3030000000, 364], [120.3116400000, 215], [120.3202800000, 214], [120.3289200000, 356], [120.3375600000, 399], [120.3462000000, 334], [120.3548400000, 348], [120.3634800000, 243], [120.3721200000, 126], [120.3807600000, 157], [120.3894000000, 288]];

		// first correct the timestamps - they are recorded as the daily
		// midnights in UTC+0100, but Flot always displays dates in UTC
		// so we have to add one hour to hit the midnights in the plot

		for (var i = 0; i < d.length; ++i) {
			d[i][0] += 60 * 60 * 1000;
		}

		// helper for returning the weekends in a period

		function weekendAreas(axes) {

			var markings = [],
				d = new Date(axes.xaxis.min);

			// go to the first Saturday

			d.setUTCDate(d.getUTCDate() - ((d.getUTCDay() + 1) % 7))
			d.setUTCSeconds(0);
			d.setUTCMinutes(0);
			d.setUTCHours(0);

			var i = d.getTime();

			// when we don't set yaxis, the rectangle automatically
			// extends to infinity upwards and downwards

			do {
				markings.push({ xaxis: { from: i, to: i + 2 * 24 * 60 * 60 * 1000 } });
				i += 7 * 24 * 60 * 60 * 1000;
			} while (i < axes.xaxis.max);

			return markings;
		}

		var options = {
			xaxis: {
				mode: "time",
				tickLength: 5
			},
			grid: {
				markings: weekendAreas
			},
			xaxis: {
				zoomRange: [0.2, 3],
				panRange: [3600119, 3600121]
			},
			yaxis: {
				zoomRange: false,
				panRange: [0, 4000]
			},
			zoom: {
				interactive: true
			},
			pan: {
				interactive: true
			}
		};

		var plot = $.plot("#placeholder", [d], options);

		var overview = $.plot("#overview", [d], {
			series: {
				lines: {
					show: true,
					lineWidth: 1
				},
				shadowSize: 0
			},
			xaxis: {
				ticks: [],
				mode: "time",
				panRange: false,
			},
			yaxis: {
				ticks: [],
				min: 0,
				autoscaleMargin: 0.1,
				panRange: false,
			},
			shift: {
				interactive: true
			}
		});

		function replot(ranges){
			if (ranges.xaxis.from != ranges.xaxis.to){
				var axis = plot.getAxes().xaxis;
				var opts = axis.options;
				opts.min = ranges.xaxis.from;
				opts.max = ranges.xaxis.to;
				plot.setupGrid();
				plot.draw();
				plot.clearSelection();
			}
		}
		// now connect the two

		$("#overview").bind("plotselected", function (event, ranges) {
			plot.setSelection(ranges);
		});

		$("#placeholder").bind("plotpan", function (event, plot) {
			var axes = plot.getAxes();
			var ranges = { xaxis: { from: axes.xaxis.min, to: axes.xaxis.max }, yaxis: { from: axes.yaxis.min, to: axes.yaxis.max } }
			overview.setSelection(ranges, true);
		});

		$("#placeholder").bind("plotzoom", function (event, plot) {
			var axes = plot.getAxes();
			var ranges = { xaxis: { from: axes.xaxis.min, to: axes.xaxis.max }, yaxis: { from: axes.yaxis.min, to: axes.yaxis.max } }
			overview.setSelection(ranges, true);
		});

		$("#overview").bind("plotshift", function (event, plot) {
			newrange = overview.getNewSelection();
			overview.setSelection(newrange, true);
			replot(newrange);
		});


	});