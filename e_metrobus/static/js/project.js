/* Project specific Javascript goes here. */


/* ROUTE */ 
let stations = [];

// add station ID to array
function saveStation(id) {
	stations.push(id);
    //console.log(stations);
	return stations;
}

// remove station ID from array
function removeStation(id) {
	stations.splice(-1,1);
    //console.log(stations);
	return stations;
}

// de-/highlight station with background-color
function highlightStation(id) {
	let station = '#' + id;
  $(station).toggleClass("highlight-station");
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
  }
  // if departure and arrival stations are selected and arrival station is tapped again -> remove arrival station
  else if (stations.length === 2 && stations[1] === this.id) {
  	removeStation(this.id);
    highlightStation(this.id);
  	//console.log("Array is 2 is same");
  }
  else {
  	//console.log("error");
  }
});
//console.log("stations: " + stations);