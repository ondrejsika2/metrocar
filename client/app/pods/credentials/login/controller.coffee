`import Ember from 'ember'`


Controller = Ember.Controller.extend

  layout: false

  actions:

    login: ->

      _this = this
      @session.authenticate('authenticator:custom',
        identification: @get('username'),
        password: @get('password')
      ).catch(->
        _this.set('hasError', true)
      )

`export default Controller`
