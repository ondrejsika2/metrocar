`import Ember from 'ember'`
`import FuelBill from 'client/app/pods/fuelbill/model'`

Route = Ember.Route.extend

  model: ->
    if @session.get('active') is false
      return @transitionTo('forbidden')
    return @store.findAll 'car'

  setupController: (controller, model) ->

    controller.set( 'carModels', model)

    controller.set( 'cars', model.map (obj) ->
        id: obj.get('id')
        text: obj.get('car_name')
    )

    fuelTypes = FuelBill.proto().FUEL_TYPES
    controller.set( 'fuels', Object.keys(fuelTypes).map (key, value) ->
        id: key
        text: fuelTypes[key]
    )

    controller.set('fuelBill', @store.createRecord('fuelbill'))

    controller.set('saveButtonText', 'Vytvořit')
    controller.set('saveButtonDisabled', false)
    controller.set('alertDanger', [])

  actions:
    willTransition: (transition) ->
      fuelBill = @get('controller.fuelBill')
      if fuelBill.get('id') is null
        fuelBill.deleteRecord();



`export default Route`
