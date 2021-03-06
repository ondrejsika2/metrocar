`import Ember from 'ember'`

Route = Ember.Route.extend

  model: ->

    return Ember.RSVP.hash(
      'user': @store.find('user', @session.get('user'))
      'userBalance': @store.find('userbalance', user: @session.get('user'))
      'journeys': @store.find('journey')
    )


  setupController: (ctrl, model) ->
    ctrl.set('user', model['user'])
    ctrl.set('user.errors', [])
    ctrl.set('userBalance', model['userBalance'].get('content')[0])
    ctrl.set('journeysCount', model['journeys'].get('content').length)

    totalDistance = 0
    model['journeys'].forEach((journey) ->
      distance = parseInt(journey.get('length'))
      totalDistance += distance
    )
    ctrl.set('totalDistance', totalDistance/1000)
    ctrl.set('alertDanger', [])

    ctrl.set('isEditable', false)


`export default Route`
