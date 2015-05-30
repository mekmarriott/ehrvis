var Med = {};
Med.colors = ["#25f"];              //blue
Med.colormod = Med.colors.length;
Med.maxRank = 0;
Med.maxWeight = 0.5;
Med.offset = 0;
// Med.offset = Med.maxWeight/2;
Med.maxItems = 15;
Med.minDate=Date.now();
Med.maxDate=0;
Med.day = 24*60*60*1000 //in milliseconds
Med.fillOpacity = 0.8; 
Med.tracks = [];
Med.drugNames = [];
Med.drugNamePreviews = [];
Med.displayNameLength = 23;
Med.dataset = [];
Med.plotOptions = {};
Med.navOptions = {};
Med.plot_height = 450;
Med.plot_height_default = 450;
Med.plot_height_max = 1000;
Med.plot_height_incr = 45;
Med.nav_height = 100;
Med.nav_height_default = 100;
Med.nav_height_incr = 10;
Med.nav_height_max = 200;


Med.truncate_name = function(name){
    if (name.length > Med.displayNameLength){
        return name.substr(0,Med.displayNameLength)+"..."
    }else{
        return name;
    }
}

Med.plot_meds = function (){
    // main plot options
    Med.plotOptions.yaxis = { min: Math.max(0,Med.maxRank-Med.maxItems), max: Med.maxRank+1, ticks: Med.drugNamePreviews, panRange: [0,Med.maxRank], zoomRange: false     };
    Med.plotOptions.xaxis = { min: Math.max(Med.minDate,Med.maxDate-90*Med.day), max: Med.maxDate, mode: 'time', panRange: [Med.minDate,Med.maxDate], zoomRange: [21*Med.day,365*Med.day]};
    Med.plotOptions.crosshair = { mode: 'none'};
    Med.plotOptions.grid = { hoverable: true, clickable: true };
    Med.plotOptions.pan = { interactive: true };
    Med.plotOptions.zoom = { interactive: true };

    // nav plot options
    Med.navOptions.yaxis = { min: 0.5, max: Med.maxRank+1, ticks:[], panRange: [0,Med.maxRank]};
    Med.navOptions.xaxis = { mode: 'time', panRange: [Med.minDate, Med.maxDate]};
    Med.navOptions.grid = { clickable: true, autoHighlight: false, markings: [] };
    Med.navOptions.selection =  { mode: null, color: "orange" }
    Med.navOptions.shift = { interactive: true };

    // $('#med_plot_target').css({height: '1500px'})

    var med_plot = $.plot('#med_plot_target',Med.dataset, Med.plotOptions);  
    var med_nav = $.plot('#med_nav_target',Med.navdataset, Med.navOptions);

    // create tooltip div 
    $("<div id=med_tooltip'></div>").css({
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
    $("#med_plot_target").bind("plothover", function (event, pos, item) {
      if (item) {
   
        ser_id = parseInt(item.series.id);
        
        var thisdose = Med.tracks[ser_id].maxdose*(Med.offset + (item.datapoint[1]-Med.tracks[ser_id].rank))/Med.maxWeight;
        thisdose = Math.round(thisdose * 100) / 100;
        var thismed = Med.tracks[ser_id].name;
        var thisdate = new Date(item.datapoint[0]);
        var curridx,presentdose;
        thisdate = thisdate.toString().substr(0,15);



        var thisunits, thismethod;
        if (!Med.tracks[ser_id].method || Med.tracks[ser_id].method=="n/a"){
            thismethod = "";
        }else{
            thismethod = "&nbsp"+Med.tracks[ser_id].method
        }

        if (!Med.tracks[ser_id].doseUnits){
            thisunits = "mg";
        }else{
            thisunits = Med.tracks[ser_id].doseUnits;
            thisunits=thisunits.replace("_"," ");
        }
        console.log(thisunits)

        if (!Med.tracks[ser_id].active){
            presentdose = "<i>(inactive)</i>";        
        }else{
            curridx = Med.tracks[ser_id].data.length - 2;
            presentdose = Med.tracks[ser_id].data[curridx][1].toString() + "&nbsp" +thisunits;
        }



        var content = thismed+ thismethod+"&#151<strong>Current:</strong> "+ presentdose+"<br><strong>Total Daily Dose:</strong> " + thisdose + "&nbsp" +thisunits + " on " + thisdate;
        $('#tooltip-replacement').html(content)


        // handle cases when close to edge of page:
        var dist_to_edge = window.innerWidth - item.pageX, ttip_pos = item.pageX+5;

        if (dist_to_edge < 250){
            ttip_pos -= (250-dist_to_edge);
        }

        $("#med_tooltip").html(content)
          .css({top: item.pageY+5, left: ttip_pos, 'background-color':'000'})
          .fadeIn(200);
      } else {
        $("#med_tooltip").hide();
      }
    });



    function replot(ranges){
        if (ranges.xaxis.from != ranges.xaxis.to){
            var x_axis = med_plot.getAxes().xaxis;
            var x_opts = x_axis.options;
            x_opts.min = ranges.xaxis.from;
            x_opts.max = ranges.xaxis.to;

            if (ranges.yaxis.from != ranges.yaxis.to){
                var y_axis = med_plot.getAxes().yaxis;
                var y_opts = y_axis.options;
                y_opts.min = ranges.yaxis.from;
                y_opts.max = ranges.yaxis.to;                
            }

            med_plot.setupGrid();
            med_plot.draw();
            med_plot.clearSelection();
        }
    }

    $("#med_nav_target").bind("plotclick", function (event, pos, item) {
      // if (item) {
        var centerPoint_x = pos.x;//item.datapoint[0];
        var centerPoint_y = pos.y;//item.datapoint[1];
        var axes = med_plot.getAxes();
        var diff_x = axes.xaxis.max - axes.xaxis.min;
        var diff_y = axes.yaxis.max - axes.yaxis.min;
        var ranges = { xaxis: { from: centerPoint_x - diff_x*0.5, to: centerPoint_x + diff_x*0.5 }, yaxis: { from: centerPoint_y - diff_y*0.5, to: centerPoint_y + diff_y*0.5 } }
        med_nav.setSelection(ranges, true);
        replot(ranges);
      // }
    });

    $("#med_nav_target").bind("plotselected", function (event, ranges) {
        med_plot.setSelection(ranges);
    });

    $("#med_plot_target").bind("plotpan", function (event, plot) {
        var axes = med_plot.getAxes();
        var ranges = { xaxis: { from: axes.xaxis.min, to: axes.xaxis.max }, yaxis: { from: axes.yaxis.min, to: axes.yaxis.max } }
        med_nav.setSelection(ranges, true);
    });

    $("#med_plot_target").bind("plotzoom", function (event, plot) {
        var axes = med_plot.getAxes();
        var ranges = { xaxis: { from: axes.xaxis.min, to: axes.xaxis.max }, yaxis: { from: axes.yaxis.min, to: axes.yaxis.max } }
        med_nav.setSelection(ranges, true);
    });

    $("#med_nav_target").bind("plotshift", function (event, plot) {
        newrange = med_nav.getNewSelection();
        med_nav.setSelection(newrange, true);
        replot(newrange);
    });

    // set initial range
    var axes = med_plot.getAxes();
    var initRange = { xaxis: { from: Math.max(Med.minDate,Med.maxDate - 90*Med.day), to: Med.maxDate }, yaxis: { from: axes.yaxis.min, to: axes.yaxis.max } }
    med_nav.setSelection(initRange, true);
    replot(initRange);


}


Med.build_dataset = function (){
    Med.dataset = [];
    Med.navdataset = [];
    for (var i = Med.tracks.length - 1; i >= 0; i--) {
        Med.dataset.push({ id: i.toString() +"lower", data: Med.tracks[i].lbound, lines: { show: true, lineWidth: 0, fill: false }, hoverable: false, color: Med.colors[i % Med.colormod] });
        Med.dataset.push({ id: i.toString() +"upper", data: Med.tracks[i].ubound, points: { show: true, radius: 1.5, symbol: "cross"}, lines: { show: true, lineWidth: 0, fill: Med.fillOpacity }, hoverable: true, color: Med.colors[i % Med.colormod],fillBetween: i.toString() +"lower"});
        Med.navdataset.push({ id: i.toString() +"lower", data: Med.tracks[i].lbound, lines: { show: true, lineWidth: 0, fill: false }, hoverable: false, color: Med.colors[i % Med.colormod] });
        Med.navdataset.push({ id: i.toString() +"upper", data: Med.tracks[i].ubound, lines: { show: true, lineWidth: 0, fill: Med.fillOpacity }, hoverable: true, color: Med.colors[i % Med.colormod],fillBetween: i.toString() +"lower"});


        Med.drugNames.push( [Med.tracks[i].rank, Med.tracks[i].name] )
        Med.drugNamePreviews.push( [Med.tracks[i].rank , Med.truncate_name(Med.tracks[i].name)] )        
    }

    return
}

Med.form_dataseries = function (medtrack){
    medtrack.ubound = owl.deepCopy(medtrack.data);
    medtrack.lbound = owl.deepCopy(medtrack.data);
    for (var i = medtrack.data.length - 1; i >= 0; i--) {
        if (medtrack.data[i]){
            medtrack.ubound[i][1]/= (medtrack.maxdose / Med.maxWeight );
            medtrack.ubound[i][1]+= medtrack.rank - Med.offset;
            medtrack.lbound[i][1]= medtrack.rank - Med.offset;
            if (medtrack.rank > Med.maxRank){
                Med.maxRank = medtrack.rank;
            }
        }
    }
}

Med.form_all_series = function(){
    for (var i = Med.tracks.length - 1; i >= 0; i--) {
        Med.form_dataseries(Med.tracks[i])
    };

}

Med.transfer_data = function(){
    Med.tracks = [];
    for (var i = medData.length - 1; i >= 0; i--) {
        Med.tracks.push( { data: medData[i].plotData, maxdose: medData[i].maxDose, rank: medData[i].rank, name: medData[i].drugName, active: medData[i].active, doseUnits: medData[i].doseUnits, method: medData[i].admMethod } )
        if (medData[i].plotData[0][0] < Med.minDate){
            Med.minDate = medData[i].plotData[0][0];
        }
    };
    Med.maxDate = Med.tracks[0].data[Med.tracks[0].data.length-2][0];
}