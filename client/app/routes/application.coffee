`import Ember from 'ember';`
`import ApplicationRouteMixin from 'simple-auth/mixins/application-route-mixin'`


Route = Ember.Route.extend ApplicationRouteMixin,

  model: ->
    if not @session.isAuthenticated
      @transitionTo('credentials.login')
    else
      console.log "app"

  actions:

    sessionAuthenticationSucceeded: ->
      @transitionTo('reservations.list')

    showModal: (name, model) ->
      @render(name,
        into: 'application',
        outlet: 'modal',
        model: model
      )

    removeModal: ->
      @disconnectOutlet(
        outlet: 'modal',
        parentView: 'application'
      )


`export default Route`
