`import Ember from 'ember';`
`import AuthenticatedRouteMixin from 'simple-auth/mixins/authenticated-route-mixin'`


Route = Ember.Route.extend AuthenticatedRouteMixin,

  beforeModel: (transition)->
    @transitionTo('reservations.list')


`export default Route`
