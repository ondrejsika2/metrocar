`import Ember from 'ember'`

McMapComponent = Ember.Component.extend

  polygonChanged: (->
    setTimeout((->

      if @get('polygon') != null

        first_lat = null
        first_lng = null

        coords = []
        for coord in @get('polygon')
          first_lat = coord[1]
          first_lng = coord[0]
          coords.push(new google.maps.LatLng(coord[1], coord[0]))

        map = new google.maps.Map(document.getElementById("map"),
          zoom: 17,
          center: new google.maps.LatLng(first_lat, first_lng)
          mapTypeId: google.maps.MapTypeId.HYBRID
        )

        metros = new google.maps.Polygon(
          paths: coords
          strokeColor: "#0000FF"
          strokeOpacity: 0.8
          strokeWeight: 2
          fillColor: "#0000FF"
          fillOpacity: 0.26
        )

        metros.setMap(map);

    ).bind(this), 1000)

  ).observes('polygon').on('didInsertElement')


`export default McMapComponent`
