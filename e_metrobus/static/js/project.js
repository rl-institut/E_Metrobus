/* Project specific Javascript goes here. */


/* ROUTE */
let stations = [];
let routeShow = [];
let stationsShow = [];

// add station ID to array
function saveStation(id) {
	stations.push(id);
    console.log(stations);
}

// remove station ID from array
function removeStation(id) {
	stations.splice(-1,1);
    console.log(stations);
}

// de-/highlight station with background-color
function highlightStation(id) {
	let station = '#' + id;
  $(station).toggleClass("highlight-station");
  $(station + " svg").toggle();
}

// highlight line route -> update SVG
function highlightSVG(stationID) {
  for (i = 0; i < stationID.length; i++) {
    $(stationID[i] + " rect").css({fill: 'red'});
  }
}

// highlight line route (stations)
function showRoute(e) {
  for (i = e[0]; i < e[1]; i++) {
    routeShow.push("#stationLine" + i);
  }
  highlightSVG(routeShow);
}

// highlight line route (between stations)
function showStations(e) {
  for (i = e[0]; i < e[1]; i++) {
    stationsShow.push("#betweenStations" + i);
  }
  highlightSVG(stationsShow);
}

// return station ID numbers without "station"
function getStationsID(e) {
  let a = [];
  for (i = 0; i < e.length; i++) {
    a[i] = e[i].slice(-2);
    // remove 0 at beginning of ID number if there
    if (a[i][0] === "0") {
      a[i] = a[i].slice(-1);
    }
    a[i] = parseInt(a[i]);
  }
  console.log("stations ID numbers: " + a);
  showRoute(a);
  showStations(a);
}

$("#stationsList .station").click(function() {
	// if no station is selected yet -> add departure station
	if (stations.length === 0) {
  	//console.log("Array is empty");
    saveStation(this.id);
    highlightStation(this.id);
  }
  // if departure station is already selected and is tapped again -> remove departure station
  else if (stations.length === 1  && stations[0] === this.id) {
  	//console.log("Array 1 is same");
    removeStation(this.id);
    highlightStation(this.id);
  }
  // if departure station is already selected and second station is tapped -> add second station as arrival station
  else if (stations.length === 1  && stations[0] !== this.id) {
  	//console.log("Array 1 is not same");
    saveStation(this.id);
    highlightStation(this.id);
    getStationsID(stations);
    console.log("stations[0]: " + stations[0]);
  }
  // if departure and arrival stations are selected and arrival station is tapped again -> remove arrival station
  else if (stations.length === 2 && stations[1] === this.id) {
  	removeStation(this.id);
    highlightStation(this.id);
    console.log("Array is 2 is same");
    console.log(stations[1]);
  }
  else {
  	//console.log("error");
  }

});
//console.log("stations: " + stations);
