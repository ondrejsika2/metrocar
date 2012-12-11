requirejs.config
  paths: OpenLayers: 'http://openlayers.org/api/OpenLayers'
  shim: OpenLayers: exports: 'OpenLayers'

define [
  'jquery'
  'OpenLayers'
], ($, OpenLayers) ->
  {
    Bounds
    Control
    Feature
    Geometry
    Layer
    Map
    Popup
    Projection
    Style
    StyleMap
  } = OpenLayers

  WSG84 = new Projection "EPSG:4326"

  styleMap = new StyleMap
    default: new Style
      # pointRadius: 10,
      # fillColor: "#ffcc66",
      strokeColor: "#ff9933",
      strokeWidth: 5,
      graphicZIndex: 1
    select: new Style
      fillColor: "#66ccff",
      strokeColor: "#3399ff",
      graphicZIndex: 2

  # Map constructor:
  (container) ->
    console.log 'initializing OL map in', container
    map = new Map()
    map.addLayer osmLayer = new Layer.OSM()
    map.zoomToMaxExtent()

    # specifying the container in the constructor doesn't seem to work
    map.render container

    # FIXME
    window.themap = map

    mapProjection = map.getProjectionObject()

    Point = ([lon, lat]) ->
      point = new Geometry.Point lon, lat
      point.transform WSG84, mapProjection
      point

    markerPopup = null

    map.addLayer routeLayer = new Layer.Vector "Route",
      styleMap: styleMap
      rendererOptions: zIndexing: true

    map.addLayer markerLayer = new Layer.Vector "Markers",
      # styleMap: styleMap
      rendererOptions: zIndexing: true

    map.addControl markerSelect = new Control.SelectFeature markerLayer,
      hover: true
    markerSelect.events.register 'featurehighlighted', map, ({feature}) ->
      console.log 'markerSelect, featurehighlighted', feature

      markerPopup = new Popup.FramedCloud "markerPopup",
        feature.geometry.getBounds().getCenterLonLat()
        null
        feature.attributes.content
        null
        true
        -> @destroy()

      feature.popup = markerPopup
      markerPopup.feature = feature
      map.addPopup markerPopup, true

    # markerSelect.events.register 'featureunhighlighted', map, ->
    #   if markerPopup
    #     setTimeout ((popup) -> -> map.removePopup popup)(markerPopup), 500

    API =
      onMoved: (callback) ->
        map.events.register 'moveend', map, -> callback API.getBounds()

      getBounds: ->
        bounds = map.getExtent()
        bounds.transform mapProjection, WSG84
        bounds

      setBounds: ({left, bottom, right, top}) ->
        bounds = new Bounds left, bottom, right, top
        bounds.transform WSG84, mapProjection
        map.zoomToExtent bounds

      drawRoute: (route) ->
        points = route.map Point
        line = new Geometry.MultiLineString points[...-1].map (point, i) ->
          new Geometry.LineString [point, points[i + 1]]

        routeFeature = new Feature.Vector line
        routeLayer.addFeatures [routeFeature]

      drawMarker: ({location, content}) ->
        point = Point location
        marker = new Feature.Vector point, content: content
        markerLayer.addFeatures [marker]
        markerSelect.activate()

      drawMarkers: (markers) -> @drawMarker m for m in markers

      clear: ->
        if markerPopup then map.removePopup markerPopup
        routeLayer.removeAllFeatures()
        markerLayer.removeAllFeatures()
