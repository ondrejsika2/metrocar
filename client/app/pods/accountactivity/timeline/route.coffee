`import Ember from 'ember'`

Route = Ember.Route.extend

  model: ->
    return @store.find('accountactivity')

  setupController: (ctrl, model) ->
    ctrl.set('accountactivities', model)


`export default Route`
