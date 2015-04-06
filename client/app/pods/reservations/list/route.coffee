`import Ember from 'ember';`
`import AuthenticatedRouteMixin from 'simple-auth/mixins/authenticated-route-mixin'`


Route = Ember.Route.extend AuthenticatedRouteMixin,

  model: ->
    console.log @get('session.user')
    return @store.findAll('reservation');

  afterModel: (model) ->
    modelId = model.get('id');
    store = @get 'store';

    return store.find('car', reservation: modelId)

  setupController: (ctrl, model) ->
    ctrl.set('reservations', model);


`export default Route`

