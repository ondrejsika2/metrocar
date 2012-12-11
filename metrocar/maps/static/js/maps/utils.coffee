{min, max} = Math

define

  boundsToPolygon: ({left, right, top, bottom}) -> [
    [left, top]
    [right, top]
    [right, bottom]
    [left, bottom]
    [left, top]
  ]

  polygonToBounds: (polygon) ->
    lats = (lat for [lon, lat] in polygon)
    lons = (lon for [lon, lat] in polygon)
    left:   min lons...
    right:  max lons...
    bottom: min lats...
    top:    max lats...

