`import Ember from 'ember'`

Route = Ember.Route.extend

  setupController: (ctrl) ->

    ctrl.set('user', @store.createRecord('registration'))

`export default Route`
