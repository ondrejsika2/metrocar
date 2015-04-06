`import Ember from 'ember'`

AccountactivityRoute = Ember.Route.extend

  model: ->

    return Ember.RSVP.hash(
      'user': @store.find('user', @session.get('user'))
      'user_balance': @store.find('userbalance', user: @session.get('user'))
    )


  setupController: (ctrl, model) ->
    console.log model
    ctrl.set('user', model['user'])
    ctrl.set('user_balance', model['user_balance'].get('content')[0])

`export default AccountactivityRoute`
