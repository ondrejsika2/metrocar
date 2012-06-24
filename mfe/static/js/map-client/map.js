/* based on the GeoExt tree example, Copyright (c) 2008-2009 The Open Source Geospatial Foundation */

var base_url = 'http://poitools.openstreetmap.de/'

var wgs84 = new OpenLayers.Projection("EPSG:4326");
var smerc = new OpenLayers.Projection("EPSG:900913");

var mapPanel, map;
var selectCtrl, popup;

var overlays = [];

function initializeMap() {
    map = new OpenLayers.Map.cdauth("map",{
        allOverlays: false,
        controls: [
            new OpenLayers.Control.LayerSwitcher(),
            new OpenLayers.Control.Navigation(),
            new OpenLayers.Control.PanZoom(),
        ],
        projection: smerc,
        displayProjection: wgs84,
        maxExtent: new OpenLayers.Bounds(-180, -90, 180, 90).transform(wgs84,smerc),
        numZoomLevels: 19,
    });
    layers = [
        new OpenLayers.Layer.cdauth.OSM.Mapnik("Mapnik"),
        new OpenLayers.Layer.cdauth.OSM.CycleMap("CycleMap"),
        new OpenLayers.Layer.cdauth.OSM.Osmarender("Osmarender"),
        //new OpenLayers.Layer.WFS("OSMI","http://tools.geofabrik.de/osmi/views/addresses/wxs?",{typename:"buildings_with_addresses", version:1.1.0"})
    ];

    map.addLayers(layers);
    map.addLayers(overlays);

	var geoLocationControl = new OpenLayers.Control.cdauth.GeoLocation();
	map.addControl(geoLocationControl);

    // Keep location.hash up to date with the current map view to provide a Permalink there. Also save the current view in a cookie.
    var hashHandler = new OpenLayers.Control.cdauth.URLHashHandler();
    map.addControl(hashHandler);
	if(hashHandler.hashHandler.getLocationHash() == "")
	{ // No Permalink has been called, use GeoLocation support
		geoLocationControl.goToGeoLocation();
	}
    if(hashHandler.hashHandler.getLocationHash() == "")
    { // Still no Permalink, use the one from the cookie (if GeoLocation works, the position might be changed to that later)
        var cookies = document.cookie.split(/;\s*/);
        for(var i=0; i<cookies.length; i++)
        {
            var equalp = cookies[i].indexOf("=");
            if(equalp == -1) continue;
            var cookie = [ cookies[i].substr(0, equalp), cookies[i].substr(equalp+1) ];
            if(cookie[0] == "osmview")
            {
                location.hash = "#"+cookie[1].replace(/&/g, ";");
                break;
            }
        }
    }
    if(hashHandler.hashHandler.getLocationHash() == "")
    { // Still no Permalink, use default values
        location.hash = "#lon=10.5;lat=51.3;zoom=5";
    }
    var cookieExpiry = new Date();
    cookieExpiry.setYear(cookieExpiry.getFullYear() + 10);
    hashHandler.events.register("hashChanged", hashHandler, function() {
        document.cookie = "osmview="+this.hashHandler.getLocationHash().replace(/;/g, "&")+";expires="+cookieExpiry.toGMTString();
    });
    hashHandler.activate();
}

Ext.onReady(function() {
    initializeMap();
    mapPanel = new GeoExt.MapPanel({
        border: true,
        region: "center",
        map: map,
	center: map.center,
	zoom: map.zoom,
    });

    var request = OpenLayers.Request.GET({ url: "treeConfig.json", async: false });
    var treeConfig = request.responseText;

    var tree = new Ext.tree.TreePanel({
        border: true,
        region: "west",
        title: "Layers",
        width: 200,
        split: true,
        collapsible: true,
        collapseMode: "mini",
        autoScroll: true,
        loader: new Ext.tree.TreeLoader({
            applyLoader: false
        }),
        root: {
            nodeType: "async",
            children: Ext.decode(treeConfig)
        },
        listeners: {
        },
        rootVisible: false,
        lines: false,
        bbar: [{
            text: "Data by OpenStreetMap",
            handler: function () {
                window.location.href="http://www.openstreetmap.org/";
            }
        }]
    });

    new Ext.Viewport({
        layout: "fit",
        hideBorders: true,
        items: {
            layout: "border",
            deferredRender: false,
            items: [mapPanel, tree, {
                contentEl: "desc",
                region: "east",
                bodyStyle: {"padding": "5px"},
                collapsible: true,
                collapseMode: "mini",
                split: true,
                width: 200,
                title: "Help"
            }]
        }
    });

    selectCtrl = new OpenLayers.Control.SelectFeature(overlays);
//    restaurants.setVisibility(false);
    mapPanel.map.addControl(selectCtrl);
    selectCtrl.activate();

});

function createPopup(feature) {
    var html = '';
    if (feature.data['id']) {
	var request = OpenLayers.Request.GET({ url: base_url+'details/'+feature.data['id'], async: false });
	html = request.responseText;
    }
    popup = new GeoExt.Popup({
        title: 'Details',
        feature: feature,
        width: 300,
        html: html,
        collapsible: false,
	unpinnable: false
    });
    popup.on({
        close: function() {
            if(!feature.layer || OpenLayers.Util.indexOf(feature.layer.selectedFeatures, this.feature) > -1) {
                selectCtrl.unselect(this.feature);
            }
        }
    });
    popup.show();
}

function createPOILayer(name,type,icon) {
    var layer = new OpenLayers.Layer.Vector(name, {
        projection: wgs84,
        maxResolution: 10.0,
        visibility: false,
        strategies: [new OpenLayers.Strategy.BBOX({ratio: 2.5})],
        protocol: new OpenLayers.Protocol.HTTP({
        url: base_url+'idlist/'+type+'.txt',
            format: new OpenLayers.Format.OSMPOI({defaultStyle: {
    				'externalGraphic': 'icons/'+icon,
    				'graphicWidth': 20,
    				'graphicHeight': 20,
    				'graphicXOffset': -10,
    				'graphicYOffset': -10,
    				'graphicOpacity': 0.7
    			}})
        }),
    });

    layer.events.on({
        featureselected: function(e) {
            createPopup(e.feature);
        }
    });

    return layer;
}

overlays.push(createPOILayer("restaurants","restaurant","restaurant.png"));
overlays.push(createPOILayer("fast food","fast_food","fastfood.png"));
overlays.push(createPOILayer("cafes","cafe","cafe.png"));
overlays.push(createPOILayer("pubs","pub","pub.png"));
overlays.push(createPOILayer("bars","bar","bar.png"));
overlays.push(createPOILayer("bakerys","bakery","bakery.png"));
overlays.push(createPOILayer("fuel stations","fuel","fuel_station.png"));
overlays.push(createPOILayer("banks","bank","bank.png"));
overlays.push(createPOILayer("ATM","atm","money_atm2.png"));
overlays.push(createPOILayer("hotels","hotel","hotel2.png"));

overlays.push(createPOILayer("post offices","post_office","post_office.png"));
overlays.push(createPOILayer("post boxes","post_box","post_box.png"));
overlays.push(createPOILayer("telephones","telephone","telephone.png"));

overlays.push(createPOILayer("museums","museum","museum.png"));
overlays.push(createPOILayer("libraries","library","library.png"));

overlays.push(createPOILayer("fire stations","fire_station","firebrigade.png"));
overlays.push(createPOILayer("police","police","police.png"));
overlays.push(createPOILayer("ambulance","ambulance","default.png"));
overlays.push(createPOILayer("doctors","doctor","doctor.png"));
overlays.push(createPOILayer("hospitals","hospital","hospital.png"));
overlays.push(createPOILayer("pharmacies","pharmacy","pharmacy.png"));
overlays.push(createPOILayer("emergency access points","emergency_access_point","default.png"));
overlays.push(createPOILayer("emergency phones","emergency_phone","default.png"));

overlays.push(createPOILayer("wikipedia articles","wikipedia","wikipedia.png"));
overlays.push(createPOILayer("websites","website","website.png"));
