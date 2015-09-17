`import Ember from 'ember'`

Controller = Ember.Controller.extend(

  actions:

    saveChanges: (param)->
      user = @get('model')
      return user.save().then(( ->
        @set('session.email', user.get('email'))
        @set('session.name', "#{user.get('first_name')} #{user.get('last_name')}")
        @set('session.username', user.get('username'))
        @set('session.active', false)
        @transitionTo('profile.success')

      ).bind(this))

)


`export default Controller`
