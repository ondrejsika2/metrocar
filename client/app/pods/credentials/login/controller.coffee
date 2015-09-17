`import Ember from 'ember'`


Controller = Ember.Controller.extend Ember.TargetActionSupport,

  layout: false

  refreshUserDetailToSession: ->
    return @get('store').find('user', @get('session.user'))
    .then(((user) ->
        @set('session.email', user.get('email'))
        @set('session.name', "#{user.get('first_name')} #{user.get('last_name')}")
        @set('session.username', user.get('username'))
      ).bind(this))

  actions:

    login: ->

      @set('loginButtonText', 'Přihlašuji se...')
      @set('loginButtonDisabled', true)

      return @session.authenticate('authenticator:custom',
        identification: @get('username'),
        password: @get('password')
      )
      .catch(((e)->
        @set('loginButtonText', 'Přihlásit se')
        @set('loginButtonDisabled', false)
        @set('errors', [@get('t')('errors.badLogin')])
      ).bind(this))


`export default Controller`
