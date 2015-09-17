`import Ember from 'ember'`
`import UnauthenticatedRouteMixin from 'simple-auth/mixins/unauthenticated-route-mixin'`

Route = Ember.Route.extend UnauthenticatedRouteMixin,


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
    ctrl.set('loginButtonText', 'Přihlásit se')
    ctrl.set('loginButtonDisabled', false)
    ctrl.set('errors', [])


`export default Route`
