`import Ember from 'ember'`


Controller = Ember.Controller.extend

  actions:
    register: ->
      user = @get('user')

      if user.get('agree') isnt true
        errorMessage = (@get('t'))('errors.agree')
        @set('user.errors.agree', [errorMessage])

      user.validate()
      .then((->
          return user.save()
          .then (->
            @transitionTo('credentials.success')
          ).bind(this)
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
