`import Ember from 'ember'`
`import UnauthenticatedRouteMixin from 'simple-auth/mixins/unauthenticated-route-mixin'`

Route = Ember.Route.extend UnauthenticatedRouteMixin,

  setupController: (ctrl) ->
    ctrl.set('user', @store.createRecord('registration'))
    ctrl.set('alertDanger', [])

`export default Route`
