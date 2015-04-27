`import Ember from 'ember'`

Controller = Ember.Controller.extend

  zoom: 11,
  centerLat: 50.0596696,
  centerLng: 14.4656239,

  reserved_time_changed: ( ->

    reserved_from = @get('reservation.reserved_from')
    reserved_until = @get('reservation.reserved_until')

    if reserved_from != undefined and reserved_until != undefined

      if moment.isMoment(reserved_from) and moment.isMoment(reserved_until)
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

  ).observes('reservation.reserved_from', 'reservation.reserved_until')

  car_change: ( ->
    carId = @get('carId.id')

    findingCar = null
    @get('carModels').forEach((car)->
      if carId == car.get('id')
        findingCar = car
    )
    @reservation.set('car', findingCar)
    @set('polygon', findingCar.get('parking.polygon'))

  ).observes('carId')

  actions:
    submit: ->

      reservation = @get('reservation')
      reservation.set('user', @get('session.user'))
      reservation.set('price', 0)

      reservation.validate()
      .then((->
          reservation.set('reserved_from', new Date(@get('reservation.reserved_from').format()))
          reservation.set('reserved_until', new Date(@get('reservation.reserved_until').format()))
          return reservation.save()
          .then (->
            @transitionTo('reservations.list')
          ).bind(this)
        ).bind(this))



`export default Controller`

