`import Ember from 'ember'`


Controller = Ember.Controller.extend

  actions:

    makeEditable: ->
      @set('isEditable', true)

    finishEditing: ->
      @get('user').save()
      @set('isEditable', false)


`export default Controller`
