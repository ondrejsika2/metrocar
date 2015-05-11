`import Ember from 'ember'`

Controller = Ember.Controller.extend

  actions:
    changePassword: ->
      oldPassword = @get('oldPassword')
      newPassword = @get('newPassword')
      newPasswordRetry = @get('newPasswordRetry')

      is_empty = false

      if !oldPassword
        @set('oldPassword_errors', [@get('t')('errors.empty')])
        is_empty = true

      if !newPassword
        @set('newPassword_errors', [@get('t')('errors.empty')])
        is_empty = true

      if !newPasswordRetry
        @set('newPasswordRetry_errors', [@get('t')('errors.empty')])
        is_empty = true

      if is_empty
        return

      if newPassword != newPasswordRetry
        @set('newPasswordRetry_errors', [@get('t')('errors.passportConfirmation')])
        return


      globalConfig = window.ENV['simple-auth'] || {}
      url = globalConfig.serverTokenEndpoint || '/api-token-auth/'

      return Ember.$.ajax({
        url: url,
        type: 'POST',
        data: {
          username: @get('session.username')
          password: oldPassword
        },
        dataType: 'json',
        contentType: 'application/x-www-form-urlencoded'
      })
      .then((->
          return @store.find('changepassword', @get('session.user'))
          .then(((user) ->
            user.set('password', newPassword)
            return user.save()
            .then((->
                return @transitionTo('profile.successpassword')
              ).bind(this))
          ).bind(this))
        ).bind(this))
      .fail(((e)->
          console.log e
          if e.hasOwnProperty('responseText')
            @set('oldPassword_errors', [@get('t')('errors.badPassword')])
        ).bind(this))

`export default Controller`
