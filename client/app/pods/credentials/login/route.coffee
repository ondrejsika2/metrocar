`import Ember from 'ember'`

Route = Ember.Route.extend


  model: ->
    if @session.isAuthenticated
      @transitionTo('reservations.list')

  renderTemplate: ->
    @render('credentials/login',
      into: 'application'
    )

  setupController: (ctrl) ->
    ctrl.set('username', '')
    ctrl.set('password', '')

`export default Route`
