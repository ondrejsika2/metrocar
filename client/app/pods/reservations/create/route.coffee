`import Ember from 'ember'`
`import AuthenticatedRouteMixin from 'simple-auth/mixins/authenticated-route-mixin'`

Route = Ember.Route.extend AuthenticatedRouteMixin,

  model: ->
    if @session.get('active') is false
      return @transitionTo('forbidden')
    return @store.findAll 'parking'

  setupController: (controller, model) ->

    controller.set('parkings', model)
    controller.set('parkingsSelect', model.map (parking) ->
      id: parking.get('id')
      text: "#{parking.get('street')} #{parking.get('land_registry_number')}, #{parking.get('city')}"
    )
    controller.set('parkingSelect', null)
    controller.set('parkingPolygon', null)

    controller.set('reservation', @store.createRecord('reservation'))

    controller.set('cars', null)
    controller.set('carsSelect', null)
    controller.set('carSelect', null)

    controller.set('saveButtonText', 'Vytvořit')
    controller.set('saveButtonDisabled', false)
    controller.set('alertDanger', [])


  actions:
    willTransition: (transition) ->
      reservation = @get('controller.reservation')
      if reservation.get('id') is null
        reservation.deleteRecord();

`export default Route`

