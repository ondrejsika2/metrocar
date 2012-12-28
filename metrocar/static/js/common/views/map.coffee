define [
  'backbone'
  'maps/utils'
], (Backbone, {boundsToPolygon, polygonToBounds}) ->


  enlargeBounds = ({left, right, top, bottom}) ->
    # Make bounds a bit larger so the displayed routes don't seem cut-off
    left: left - 0.01
    right: right + 0.01
    top: top + 0.01
    bottom: bottom - 0.01


  class Map extends Backbone.View
    ###
    A generic map view.
    ###

    initialize: ({MapModule}) ->
      ###
      MapModule should be an module implementing a map wrapper, such as maps/ol
      ###
      @map = MapModule.createMap @el
      @map.onMoved (bounds) => @trigger 'change', boundsToPolygon bounds

    getValue: -> boundsToPolygon enlargeBounds @map.getBounds()

    setValue: (polygon) -> @map.setBounds polygonToBounds polygon
