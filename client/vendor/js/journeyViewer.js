window.loadAndDrawJourney = function(data, el){

	console.log("Starting Journey JSON datafile processing");

  //
  var journeyData = data;
  window.TTM = {};
  window.m = null; // globální objekt mapy

  // heading
  addJourneyHeading(data.TripDetailsInfo);

  // nakreslíme graf
  jQuery.getScript("https://api.mapy.cz/loader.js", function(data, textStatus, jqxhr){

    // načteme mapy.cz API
    Loader.async=true;
    Loader.load(null, {}, function(){

      // postavíme html strukturu
      buildContainers(journeyData.TripDetailsHead, el);

      // naparsujeme - již zde potřebujeme mapy.cz
      // - uložíme v globální proměnné window.TTM
      parseData(journeyData.TripDetailsLog);

      // kreslení
      window.drawChart();
    });
  });
}

window.addJourneyHeading = function(info){

		// datum startu
		var stringDate = getDateAsString(info.start);

		// čas
		var totalSeconds = info.time;
		var h = Math.floor(totalSeconds / 3600);
		totalSeconds %= 3600;
		var m = Math.floor(totalSeconds / 60);
		var s = totalSeconds % 60;
		var totalTime = h+" h "+m+" min "+s+" s";

		// vzdálenost
		var dist = info.distance / 1000;
		var niceDist = Math.round(info.distance/10);
		niceDist = niceDist / 100;

		// rychlost
		var avgSpeed = dist / (info.time / 3600);
		avgSpeed = Math.round(avgSpeed*100);
		avgSpeed = avgSpeed/100;

		// přidáme data do záhlaví
		var infoRow = $(".journey-info");
		infoRow.append("<span style='margin-right: 20px; margin-bottom:15px; display:inline-block;'>"+"Datum: "+stringDate+"</span>");
		infoRow.append("<span style='margin-right: 20px; margin-bottom:15px; display:inline-block;'>"+"Celkový čas: "+totalTime+"</span>");
		infoRow.append("<span style='margin-right: 20px; margin-bottom:15px; display:inline-block;'>"+"Vzdálenost: "+niceDist+" km</span>");
		infoRow.append("<span style='margin-right: 20px; margin-bottom:15px; display:inline-block;'>"+"Prům. rychlost: "+avgSpeed+" km/h</span>");
}



window.getDateAsString = function(timestamp){
  var a = new Date(timestamp);
  var year = a.getFullYear();
  var month = a.getMonth()+1;
  var date = a.getDate();
  var hour = a.getHours();
  if(hour < 10){ hour = "0" + sec;}
  var min = a.getMinutes();
  if(min < 10){ min = "0" + sec;}
  var sec = a.getSeconds();
  if(sec < 10){ sec = "0" + sec;}
  var time = date + '.' + month + '.' + year + ' ' + hour + ':' + min + ':' + sec ;
  return time;
}




// postaví kontejnery
window.buildContainers = function(headData, el){

	// mapa
	window.TTM["gps"] = {divID: "m"};
	el.append($("<div id='m' style='height:380px'></div><br />"));

	//
	console.log(headData);

	// gps
	window.TTM["gps_acc"] = {divID: "g_gps_acc", name: "Přesnost GPS"};
	el.append($("<b class=''>Přesnost GPS</b> (m)<br />"));
	el.append($("<div id='g_gps_acc' style='height:380px'></div><br />"));
	window.TTM["gps_alt"] = {divID: "g_gps_alt", name: "Nadmořská výška GPS"};
	el.append($("<b class=''>Nadmořská výška GPS</b> (m)<br />"));
	el.append($("<div id='g_gps_alt' style='height:380px'></div><br />"));

	// accel
	window.TTM["accel_x"] = {divID: "g_accel_x", name: "Akcelerace X"}
	el.append($("<b class=''>Akcelerace X</b> (m*s^-2)<br />"));
	el.append($("<div id='g_accel_x' style='height:380px'></div><br />"));
	window.TTM["accel_y"] = {divID: "g_accel_y", name: "Akcelerace Y"}
	el.append($("<b class=''>Akcelerace Y</b> (m*s^-2)<br />"));
	el.append($("<div id='g_accel_y' style='height:380px'></div><br />"));
	window.TTM["accel_z"] = {divID: "g_accel_z", name: "Akcelerace Z"}
	el.append($("<b class=''>Akcelerace Z</b> (m*s^-2)<br />"));
	el.append($("<div id='g_accel_z' style='height:380px'></div><br />"));
	window.TTM["accel_total"] = {divID: "g_accel_total", name: "Akcelerace Total"}
	el.append($("<b class=''>Akcelerace Total</b> (m*s^-2)<br />"));
	el.append($("<div id='g_accel_total' style='height:380px'></div><br />"));

	// gps - speed
	window.TTM["gps_speed"] = {divID: "g_gps_speed", name: "Rychlost GPS"};
	el.append($("<b class=''>Rychlost GPS</b> (km/h)<br />"));
	el.append($("<div id='g_gps_speed' style='height:380px'></div><br />"));

	// další tagy (OBD)
	for( var index =0; index < headData.length; index++ ){
      console.log(headData[index].tag);
      window.TTM[headData[index].tag] = {divID: "g_" + headData[index].tag, name: "" + headData[index].name};
      el.append($("<b class=''>" + headData[index].tag + "</b><br />"));
      el.append($("<div id='g_" + headData[index].tag + "' style='height:380px'></div><br />"));
	}

	//el.append($("<div id='g_rpm' style='height:380px'></div><br />"));
	//el.append($("<div id='g_speed' style='height:380px'></div><br />"));

}


// přečte data z JSON souboru
window.parseData = function(arr){

	// připravíme  místo pro data a čas. známky
	for(key in window.TTM){
		if(key == "gps"){
			window.TTM[key]["data"] = {stamps:[], values:[]};
		}else{
			window.TTM[key]["data"] = [];
		}
	}

	// časová konzistence
	var lastTime = 0;
	var newTime = 0;

	var q = 0;
	var json;
	var mega = 1000000;
	for( key in arr ){

		// naparsujeme JSON data
    try {
      json = JSON.parse(arr[key]["json"]);
      time = parseFloat(arr[key]["time"]);
      aDate = new Date(time);
    }catch(error){
      console.log(error);
    }

		//debug
		/*if(q < 50){
			console.log(arr[key]);
			q++;
			console.log(json["total"]);
		}*/

		// přidáme gps data
		if(arr[key]["type"] == "gps"){

			// gps poloha
			window.TTM["gps"]["data"]["values"].push(
				SMap.Coords.fromWGS84(
					parseFloat(json["long"])/mega,
					parseFloat(json["lat"])/mega
				)
			);
			window.TTM["gps"]["data"]["stamps"].push(
				aDate
			);

			// gps přesnost
			window.TTM["gps_acc"]["data"].push([
				aDate,
				parseFloat(json["acc"])
			]);

			// gps výška
			window.TTM["gps_alt"]["data"].push([
				aDate,
				parseFloat(json["alt"])
			]);

			// gps rychlost
			window.TTM["gps_speed"]["data"].push([
				aDate,
				parseFloat(json["speed"])
			]);

			continue;
		}

		// data z akcelerometru
		if(arr[key]["type"] == "accel"){

			// x
			window.TTM["accel_x"]["data"].push([
				aDate,
				parseFloat(json["x"])
			]);

			// y
			window.TTM["accel_y"]["data"].push([
				aDate,
				parseFloat(json["y"])
			]);

			// z
			window.TTM["accel_z"]["data"].push([
				aDate,
				parseFloat(json["z"])
			]);

			// total
			window.TTM["accel_total"]["data"].push([
				aDate,
				parseFloat(json["total"])
			]);

			continue;
		}

		// přidáme obd data
		var type = arr[key]["type"];
		if(window.TTM[type] != null){
			// total
			window.TTM[type]["data"].push([
				aDate,
				parseFloat(json[type])
			]);
		}
	}

	console.log(window.TTM["gps"]);

	//
	//return response;
}


// zakreslí GPS data do mapy
// from, to - vybranná oblast
window.drawLogToMap = function(gpsPoints, gpsStamps, from, to){

	if(window.TTM.mapParams == null){
		window.TTM.mapParams = {from: from, to: to}
	}else{
		if((window.TTM.mapParams.from == from) && (window.TTM.mapParams.to == to)){
			return;
		}
	}

	//
	window.TTM.mapParams.from = from;
	window.TTM.mapParams.to = to;

	console.log("Drawing to map");
	console.log("from: "+from);
	console.log("to: "+to);

	// rozdělím data do tří skupin -> před selekcí, selekce a po selekci
	gpsPointsPre = [];
	gpsPointsSelected = [];
	gpsPointsPost = [null];

	// pokud nemáme from a to (inicializace), vše dáme do pre
	if(from == null){
		gpsPointsPre = gpsPoints;
	}else{

		// jinak rozdělíme
		for(var i=0; i < gpsPoints.length; i++){
			if(gpsStamps[i] < from){
				gpsPointsPre.push(gpsPoints[i]);

			}else{
				if(gpsStamps[i] > to){
					gpsPointsPost.push(gpsPoints[i]);
				}else{
					gpsPointsSelected.push(gpsPoints[i]);
				}
			}
		}

		// spojíme krajní body intervalů
		if(gpsPointsPre.length > 0 && gpsPointsSelected.length > 0){
			gpsPointsPre.push(gpsPointsSelected[0]);
		}
		if(gpsPointsPost.length > 1 && gpsPointsSelected.length > 0){
			gpsPointsPost[0] = gpsPointsSelected[gpsPointsSelected.length-1];
		}else{
			gpsPointsPost = [];
		}
	}

	console.log("Pre");
	console.log(gpsPointsPre);

	console.log("Sel");
	console.log(gpsPointsSelected);

	console.log("Post");
	console.log(gpsPointsPost);

	console.log("Stamps");
	console.log(gpsStamps);

	// vytvoříme mapu v div#m
	//window.m = new SMap(JAK.gel("m"), cAz[0], cAz[1]);
	if(window.m == null){
		window.m = new SMap(JAK.gel("m"));
		window.m.addDefaultLayer(SMap.DEF_BASE).enable();
		window.m.addDefaultControls();
	}else{
		window.m.removeLayer(window.mlayer);
	}

	// spočítáme a nastavíme střed a zoom mapy
	//var cAz = window.m.computeCenterZoom(gpsPoints, false);
	//window.m.setCenterZoom(cAz[0], cAz[1]);

	// připravíme vrstvu geometrie
	window.mlayer = new SMap.Layer.Geometry();
	window.m.addLayer(window.mlayer);
	window.mlayer.enable();

	// přidáme pre body do vrstvy
	var polylinePre = new SMap.Geometry(SMap.GEOMETRY_POLYLINE, null, gpsPointsPre, {
		color: "#00f",
		width: 3
	});
	window.mlayer.addGeometry(polylinePre);

	// přidáme i ostatní
	if(from != null){

		// vybranné
		var polylineSel = new SMap.Geometry(SMap.GEOMETRY_POLYLINE, null, gpsPointsSelected, {
			color: "#f00",
			width: 3
		});
		window.mlayer.addGeometry(polylineSel);

		// post
		var gpsPointsPost = new SMap.Geometry(SMap.GEOMETRY_POLYLINE, null, gpsPointsPost, {
			color: "#00f",
			width: 3
		});
		window.mlayer.addGeometry(gpsPointsPost);
	}

	// spočítáme a nastavíme střed a zoom mapy
	if(from == null){
		var cAz = window.m.computeCenterZoom(gpsPointsPre, false);
		window.m.setCenterZoom(cAz[0], cAz[1]);
	}else{
		var cAz = window.m.computeCenterZoom(gpsPointsSelected, false);
		window.m.setCenterZoom(cAz[0], cAz[1]);
	}


}

window.onRangeSelected = function(me, initial){

	// máme zazoomováno?
	if(!me.isZoomed()){

		// ne -> překreslíme bez výběru
		drawLogToMap(
			window.TTM["gps"]["data"]["values"],
			window.TTM["gps"]["data"]["stamps"],
			null, null);
		return;
	}

	// zjistíme oblast výběru
	var selection = me.xAxisRange();
	var from = selection[0];
	var to = selection[1];

	// nakreslíme mapu
	drawLogToMap(
		window.TTM["gps"]["data"]["values"],
		window.TTM["gps"]["data"]["stamps"],
		from, to);
}

window.drawChart = function (obdValues){



	// grafy
	charts = [];

	//
	for(key in window.TTM){

		if(key == "gps"){continue;}

		charts.push(
			new Dygraph(document.getElementById(window.TTM[key]["divID"]), window.TTM[key]["data"], {
				drawPoints: true,
				showRangeSelector: true,
				labels: ['Čas', window.TTM[key]["name"]]
			})
		);
	}

	// synchronizace
	var sync = Dygraph.synchronize(charts,{
	  zoom: true,
	  selection: true,
	  callback: onRangeSelected
	});
}
