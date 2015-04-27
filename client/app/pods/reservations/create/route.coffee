`import Ember from 'ember'`
`import AuthenticatedRouteMixin from 'simple-auth/mixins/authenticated-route-mixin'`

Route = Ember.Route.extend AuthenticatedRouteMixin,

  model: ->
    return @store.findAll 'car'

  afterModel: (cars) ->
    store = @get('store')
    promises = []
    cars.forEach((car)->
      promises.push(store.find('parking', car.get('parking.id')))
    )
    return Ember.RSVP.all(promises)

  setupController: (controller, model) ->

    controller.set( 'carModels', model)

    controller.set( 'cars', model.map (obj) ->
      id: obj.get('id')
      text: obj.get('car_name')
    )

    controller.set 'model', Ember.A([
      title: 'Škoda Fabia Zelená',
      lat: 50.036262,
      lng: 14.518328
    ])

    controller.set('reservation', @store.createRecord('reservation'))

`export default Route`

