requirejs.config
  paths: OpenLayers: 'http://openlayers.org/api/OpenLayers'
  shim: OpenLayers: exports: 'OpenLayers'

define [
  'jquery'
  'OpenLayers'
  'maps/utils'
], ($, OpenLayers, utils) ->
  {
    Control
    Feature
    Geometry
    Icon
    Layer
    Map
    Marker
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
      strokeColor: "#F80101",
      strokeWidth: 5,
      graphicZIndex: 1
    select: new Style
      fillColor: "#66ccff",
      strokeColor: "#3399ff",
      graphicZIndex: 2

  OLTransformType = (T, projection) -> (args...) ->
    obj = new T args...
    obj.transform WSG84, projection
    obj

  createPopup = (map, location, content) ->
    markerPopup = new Popup.FramedCloud "popup",
      location
      null
      content
      null
      true
      -> @destroy()
    map.addPopup markerPopup, true

  createMap = (container) ->
    console?.debug 'initializing OL map in', container
    map = new Map()
    map.addLayer osmLayer = new Layer.OSM()
    map.zoomToMaxExtent()

    # specifying the container in the constructor doesn't seem to work
    map.render container

    # FIXME
    window.themap = map

    mapProjection = map.getProjectionObject()

    # shortcuts to create OL types that need coordinate transformation
    typeConstructor = (T) -> OLTransformType T, mapProjection
    Point = typeConstructor OpenLayers.Geometry.Point
    LonLat = typeConstructor OpenLayers.LonLat
    Bounds = typeConstructor OpenLayers.Bounds

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
      location = feature.geometry.getBounds().getCenterLonLat()
      content = feature.attributes.content
      createPopup map, location, content

    map.addLayer iconMarkerLayer = new Layer.Markers "IconMarkers",
      rendererOptions: zIndexing: true

    API =
      onMoved: (callback) ->
        map.events.register 'moveend', map, -> callback API.getBounds()

      getBounds: ->
        bounds = map.getExtent()
        bounds.transform mapProjection, WSG84
        bounds

      setBounds: ({left, bottom, right, top}) ->
        # bounds = new Bounds left, bottom, right, top
        # bounds.transform WSG84, mapProjection
        map.zoomToExtent Bounds left, bottom, right, top

      drawRoute: (route) ->
        points = route.map ([x, y]) -> Point x, y
        line = new Geometry.MultiLineString points[...-1].map (point, i) ->
          new Geometry.LineString [point, points[i + 1]]

        routeFeature = new Feature.Vector line
        routeLayer.addFeatures [routeFeature]

      drawMarker: ({location, content}) ->
        point = Point location...
        marker = new Feature.Vector point, content: content
        markerLayer.addFeatures [marker]
        markerSelect.activate()

      drawIconMarker: ({location, content, icon, size, offset}) ->
        ###
        content: HTML content of a pop-up
        icon: URL to icon image
        size: [x, y] pixels
        offset: (optional) [x, y] pixels
        ###
        _size = new OpenLayers.Size size...
        _offset = new OpenLayers.Pixel (offset or [-size[0] / 2, -size[1]])...
        _icon = new OpenLayers.Icon icon, _size, _offset
        _location = LonLat location...
        iconMarkerLayer.addMarker marker = new Marker _location, _icon
        marker.events.register 'click', map, ->
          createPopup map, _location, content
          # markerPopup = new Popup.FramedCloud "markerPopup",
          #   _location
          #   null
          #   content
          #   null
          #   true
          #   -> @destroy()

          # map.addPopup markerPopup, true

      drawMarkers: (markers) -> @drawMarker m for m in markers

      clear: ->
        if markerPopup then map.removePopup markerPopup
        routeLayer.removeAllFeatures()
        markerLayer.removeAllFeatures()
        iconMarkerLayer.clearMarkers()

      focus: (locations) ->
        console.log 'OLMap focus called with', locations
        API.setBounds utils.polygonToBounds locations
        # {left, bottom, right, top} = utils.polygonToBounds locations
        # map.zoomToExtent Bounds left, bottom, right, top

  {createMap}
