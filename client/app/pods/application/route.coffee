`import Ember from 'ember';`
`import ApplicationRouteMixin from 'simple-auth/mixins/application-route-mixin'`


Route = Ember.Route.extend ApplicationRouteMixin,

  model: ->
    if @session.isAuthenticated
      return @refreshUserDetailToSession()


  refreshUserDetailToSession: ->
    return @get('store').find('user', @get('session.user'))
    .then(((user) ->
        @set('session.email', user.get('email'))
        @set('session.name', "#{user.get('first_name')} #{user.get('last_name')}")
        @set('session.username', user.get('username'))
        @set('session.active', user.get('active'))
      ).bind(this))

  actions:
    sessionAuthenticationSucceeded: ->
      return @refreshUserDetailToSession()
      .then((->
          @transitionTo('reservations.list')
        ).bind(this))

    invalidateSession: ->
      @get('session').invalidate();
      @transitionTo('credentials.login')


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
