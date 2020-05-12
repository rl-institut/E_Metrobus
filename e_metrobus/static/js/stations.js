/* ROUTE */
let stations = [];

// add station ID to array
function saveStation(id) {
	stations.push(id);
}

// remove station ID from array
function removeStation(id) {
    const index = stations.indexOf(id);
    if (index > -1) {
      stations.splice(index, 1);
    }
}

// un-/highlight station with background-color
function highlightStation(id) {
  let station = '#' + id;
  $(station).toggleClass("highlight-station");
  $(station + " svg").toggle();
}

function showLines(show) {
  let color = '#000000'
  if (!show) {
    color = '#EFEFEF'
  }

  let station_ids = getStationIDs()
  let start = station_ids[0]
  let end = station_ids[1]
  if (station_ids[0] > station_ids[1]) {
    start = station_ids[1]
    end = station_ids[0]
  }
  for (i = start; i < end; i++) {
    $("#line" + i + " rect").css({fill: color});
    $("#betweenStations" + i + " rect").css({fill: color});
  }
}

// return station ID numbers without "station"
function getStationIDs() {
  let a = [];
  for (i = 0; i < stations.length; i++) {
    a[i] = stations[i].slice(-2);
    // remove 0 at beginning of ID number if there
    if (a[i][0] === "0") {
      a[i] = a[i].slice(-1);
    }
    a[i] = parseInt(a[i]);
  }
  return a
}

$("#stationsList .station").click(function() {
  if (stations.length == 2 && !stations.includes(this.id)) {
     showLines(false);
     for (i = 0; i < stations.length; i++) {
        highlightStation(stations[i])
     }
     stations = [];
  }
  if (stations.includes(this.id)) {
  	showLines(false);
    removeStation(this.id);
    highlightStation(this.id);
  } else {
    saveStation(this.id);
    highlightStation(this.id);
  }

  //Show button if 2 stations are selected
  if (stations.length === 2) {
    showLines(true);
    $("#station_form").show();
  } else {
    $("#station_form").hide();
  }

});

function post() {
  if (stations.length === 2) {
    $('#stations').val(stations);
    $('#stations_form').submit();
  }
}
