`import Ember from 'ember'`

Route = Ember.Route.extend

  model: ->
    return @get('store').findQuery('accountactivity', { page: 1 })

  setupController: (ctrl, model) ->
    ctrl.set('accountactivities', model)
    ctrl.set('totalPages', model.get('meta.pages'))


`export default Route`
