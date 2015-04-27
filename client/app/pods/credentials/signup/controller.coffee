`import Ember from 'ember'`


Controller = Ember.Controller.extend

  actions:
    register: ->
      user = @get('user')

      user.validate()
      .then((->
        return user.save()
        .then (->
          @transitionTo('credentials.success')
        ).bind(this)
        .catch((e) ->

          console.log e
        )

        ).bind(this))
      .catch(((e)->
        if e.hasOwnProperty('responseText')
          user_errors = @get('user.errors')
          errors = JSON.parse(e.responseText)
          for error_name of errors
            user_errors.set(error_name, [errors[error_name]]);

        ).bind(this))


`export default Controller`
