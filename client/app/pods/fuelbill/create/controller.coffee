`import Ember from 'ember'`


Controller = Ember.Controller.extend

  actions:

    makeEditable: ->
      @set('isEditable', true)

    finishEditing: ->
      @set('isEditable', false)


`export default Controller`
