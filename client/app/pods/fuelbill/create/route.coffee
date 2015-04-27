`import Ember from 'ember'`
`import FuelBill from 'client/app/pods/fuelbill/model'`

Route = Ember.Route.extend

  model: ->
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

    controller.set('fuel_bill', @store.createRecord('fuelbill'))




`export default Route`
