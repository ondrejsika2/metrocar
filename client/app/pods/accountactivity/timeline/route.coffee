`import Ember from 'ember'`

Route = Ember.Route.extend

  model: ->
    return @store.find('accountactivity')

  setupController: (ctrl, model) ->
    console.log model
    ctrl.set('accountactivities', model)


`export default Route`
