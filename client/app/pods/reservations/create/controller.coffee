`import Ember from 'ember'`

Controller = Ember.Controller.extend

  zoom: 11,
  centerLat: 50.0596696,
  centerLng: 14.4656239,

  parkingIdChanged: Ember.observer('parkingSelect', 'reservation.reserved_from', 'reservation.reserved_until', ->

    if @get('parkingSelect') != null and @get('reservation.parking') != @get('parkingSelect')

      foundParking = null
      parkingSelectId = @get('parkingSelect.id')

      @get('parkings').forEach((parking)->
        if parkingSelectId == parking.get('id')
          foundParking = parking
      )
      @set('reservation.parking', foundParking)
      @set('parkingPolygon', foundParking.get('polygon'))

    reservedFrom = @get('reservation.reserved_from')
    reservedUntil = @get('reservation.reserved_until')
    parking = @get('reservation.parking')

    if reservedFrom != undefined and reservedUntil != undefined and parking != null

      if moment.isMoment(reservedFrom) and moment.isMoment(reservedUntil)
        @store.find('car',
          reserved_from: reservedFrom.format('YYYY-MM-DD, HH:mm:ss')
          reserved_until: reservedUntil.format('YYYY-MM-DD, HH:mm:ss')
          parking: parking.get('id')
        ).then(((cars)->
            @set('cars', cars)
            @set('carsSelect', cars.map (obj) ->
                id: obj.get('id')
                text: obj.get('car_name')
            )
          ).bind(this)
        )

  )

  car_change: Ember.observer('carSelect',  ->
    if @get('cars')
      carSelectId = @get('carSelect.id')

      foundCar = null
      @get('cars').forEach((car)->
        if carSelectId == car.get('id')
          foundCar = car
      )
      @reservation.set('car', foundCar)
      @set('polygon', foundCar.get('parking.polygon'))

  )

  actions:
    submit: ->

      @set('saveButtonText', 'Ukládám...')
      @set('saveButtonDisabled', true)

      reservation = @get('reservation')
      reservation.set('user', @get('session.user'))
      reservation.set('price', 0)

      reservation.validate()
      .then((->
          if (@get('reservation.reserved_from')._isAMomentObject)
            reservation.set('reserved_from', new Date(@get('reservation.reserved_from').format()))
          if (@get('reservation.reserved_until')._isAMomentObject)
            reservation.set('reserved_until', new Date(@get('reservation.reserved_until').format()))

          return reservation.save()
          .then (->
            @transitionTo('reservations.list')
          ).bind(this)
        ).bind(this))
      .catch(((e)->
          @set('saveButtonText', 'Vytvořit')
          @set('saveButtonDisabled', false)
          if e and e.hasOwnProperty('responseText')
            reservationErrors = @get('reservation.errors')
            errors = JSON.parse(e.responseText)

            if errors.hasOwnProperty('detail')
              @set('alertDanger', errors.detail)
            else
              for errorName of errors
                reservationErrors.set(errorName, [errors[errorName]]);
        ).bind(this))



`export default Controller`

