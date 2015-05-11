`import Ember from 'ember'`


Controller = Ember.Controller.extend

  car_change: ( ->
    carId = @get('carId.id')

    findingCar = null
    @get('carModels').forEach((car)->
      if carId == car.get('id')
        findingCar = car
    )
    @fuelBill.set('car', findingCar)
    @set('polygon', findingCar.get('parking.polygon'))

  ).observes('carId')

  fuel_change: ( ->
    @fuelBill.set('fuel', @get('fuelId.id'))
  ).observes('fuelId')

  actions:
    submit: ->
      @set('saveButtonText', 'Ukládám...')
      @set('saveButtonDisabled', true)

      fuelBill = @get('fuelBill')
      fuelBill.set('datetime', new Date())

      file = document.getElementById('file-field').files[0];
      fuelBill.set('image', file)

      @store.find('userbalance', user: @get('session.user'))
      .then(((accounts) ->
          account_id = accounts.get('content')[0].get('id')
          fuelBill.set('account', account_id)

          fuelBill.validate()
          .then((->
              return fuelBill.save()
              .then (->
                @transitionTo('fuelbill.list')
              ).bind(this)
            ).bind(this))
          .catch(((e)->
              @set('saveButtonText', 'Vytvořit')
              @set('saveButtonDisabled', false)
              if e.hasOwnProperty('responseText')
                fuelBillErrors = @get('fuelBill.errors')
                errors = JSON.parse(e.responseText)
                if errors.hasOwnProperty('detail')
                  @set('alertDanger', errors.detail)
                else
                  for errorName of errors
                    fuelBillErrors.set(errorName, [errors[errorName]]);
            ).bind(this))
        ).bind(this))


`export default Controller`
