`import Ember from 'ember'`

Route = Ember.Route.extend

  model: ->
    return @store.find('fuelbill')


  setupController: (ctrl, model) ->
    ctrl.set('fuelbills', model)

`export default Route`
