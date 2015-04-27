`import Ember from 'ember';`
`import ApplicationRouteMixin from 'simple-auth/mixins/application-route-mixin'`


Route = Ember.Route.extend ApplicationRouteMixin,

#  beforeModel: (transition)->
#    console.log transition
#    console.log transition.handlerInfos[2].name != 'credentials.login'
#
#    if not @session.isAuthenticated and transition.handlerInfos[1].name == 'credentials' and transition.handlerInfos[2].name != 'credentials.login'
#      return
#
#    if not @session.isAuthenticated
#      @transitionTo('credentials.login')

  model: ->
#    if not @session.isAuthenticated
#      @transitionTo('credentials.login')

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
