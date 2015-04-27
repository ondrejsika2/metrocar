`import Ember from 'ember'`
`import EmberValidations from 'ember-validations'`

Controller = Ember.Controller.extend EmberValidations.Mixin,

  actions:

    makeEditable: ->
      @set('isEditable', true)

    finishEditing: ->

      user = @get('user')

      user.validate()
        .then((->
          user.save()
          @set('isEditable', false)
        ).bind(this))



`export default Controller`
