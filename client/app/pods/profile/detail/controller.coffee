`import Ember from 'ember'`
`import EmberValidations from 'ember-validations'`

Controller = Ember.Controller.extend EmberValidations.Mixin,

  actions:
    makeEditable: ->
      @set('doNothingWithIdentityCardImage', true)
      @set('doNothingWithDriversLicenceImage', true)
      @set('isEditable', true)

    deleteIdentityCardImage: ->
      @set('doNothingWithIdentityCardImage', false)
      @set('user.identity_card_image', null)

    deleteDriversLicenceImage: ->
      @set('doNothingWithDriversLicenceImage', false)
      @set('user.drivers_licence_image', null)


    finishEditing: ->
      user = @get('user')

      user.set('retry_password', user.get('password'))

      return user.validate()
      .then((->

          if user.get('isDirty') is false
            @set('isEditable', false)
            @set('user.errors', [])
            return

          return user.save().then(( ->
            @set('isEditable', false)
            @set('session.email',@get('user.email'))
            @set('session.name', "#{@get('user.first_name')} #{@get('user.last_name')}")
            @set('session.username', @get('user.username'))
            @set('session.active', false)
            @transitionTo('profile.success')
          ).bind(this))

        ).bind(this))
      .catch(((e)->
          if e.hasOwnProperty('responseText')
            userErrors = @get('user.errors')
            errors = JSON.parse(e.responseText)
            if errors.hasOwnProperty('detail')
              @set('alertDanger', errors.detail)
            else
              for errorName of errors
                userErrors.set(errorName, [errors[errorName]]);

        ).bind(this))

`export default Controller`
