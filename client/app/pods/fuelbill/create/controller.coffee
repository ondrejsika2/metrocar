`import Ember from 'ember'`


Controller = Ember.Controller.extend

  car_change: ( ->
    carId = @get('carId.id')

    findingCar = null
    @get('carModels').forEach((car)->
      if carId == car.get('id')
        findingCar = car
    )
    @fuel_bill.set('car', findingCar)
    @set('polygon', findingCar.get('parking.polygon'))

  ).observes('carId')

  fuel_change: ( ->

    @fuel_bill.set('fuel', @get('fuelId.id'))
  ).observes('fuelId')

  actions:
    submit: ->
      fuel_bill = @get('fuel_bill')
      fuel_bill.set('datetime', new Date())

      file = document.getElementById('file-field').files[0];
      fuel_bill.set('image', file)

      @store.find('userbalance', user: @get('session.user'))
      .then((accounts) ->
        account_id = accounts.get('content')[0].get('id')
        fuel_bill.set('account', account_id)
        fuel_bill.save()
      )


`export default Controller`
