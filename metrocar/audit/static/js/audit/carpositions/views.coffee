define [
  'module'
  'backbone'
  'maps/ol'
  'common/views/map'
  'common/views/select'
], (module, Backbone, OLMap, MapView, Select) ->

  config = module.config()


  class Map extends MapView

    display: (data) ->
      @map.clear()
      for {location, cars} in data
        @map.drawIconMarker
          location: location
          content: cars
          icon: "#{config.staticUrl}img/icons/car.png"
          size: [32, 32]
          offset: [-16, -16]

    focus: (data, zoom) -> @map.focus (data.map (x) -> x.location), zoom


  class App extends Backbone.View

    initialize: ->
      @map = new Map el: @$('.map'), MapModule: OLMap
      @map.on 'change', =>
        console.log 'map change occured'
        @update()
      @showAll()

      @carSelect = new Select el: @$('.car-select')
      @carSelect.on 'change', (carId) =>
        @query {car_id: carId}, (response) => @map.focus response, 12

    update: ->
      data = in_polygon: @map.getValue()
      @query data, (response) => @map.display response

    query: (data, callback) ->
      $.post config.dataUrl, JSON.stringify(data), callback

    showAll: -> @query {}, (response) => @map.focus response

  {App}
