`import Ember from 'ember'`

Controller = Ember.Controller.extend

  zoom: 11,
  centerLat: 50.0596696,
  centerLng: 14.4656239,

  reserved_time_changed: ( ->

    reserved_from = @get('reserved_from')
    reserved_until = @get('reserved_until')

    if reserved_from != undefined and reserved_until != undefined
      @store.find('car',
        reserved_from: reserved_from.format('YYYY-MM-DD, HH:mm:ss')
        reserved_until: reserved_until.format('YYYY-MM-DD, HH:mm:ss')
      ).then(((cars)->
          @set('carModels', cars)
          @set('cars', cars.map (obj) ->
              id: obj.get('id')
              text: obj.get('car_name')
          )
        ).bind(this)
      )

    console.log @get('reserved_from')

  ).observes('reserved_from', 'reserved_until')

  car_change: ( ->
    carId = @get('carId.id')

    console.log @get('carModels')

    findingCar = null
    @get('carModels').forEach((car)->
      if carId == car.get('id')
        findingCar = car
    )
    console.log findingCar.get('parking.polygon')
    @set('polygon', findingCar.get('parking.polygon'))

  ).observes('carId')

  actions:
    submit: ->
      reserved_from = new Date(@get('reserved_from').format())
      reserved_until = new Date(@get('reserved_until').format())
      user = @get('session.user')

      @store.find('car', @get('carId.id'))
      .then ((car)->
        reservation = @store.createRecord('reservation',
          'car': car
          'reserved_from': reserved_from
          'reserved_until': reserved_until,
          'user': user,
          'price': 0,
        )
        return reservation.save()
        .then (->
          @transitionTo('reservations.list')
        ).bind(this)
      ).bind(this)


`export default Controller`

