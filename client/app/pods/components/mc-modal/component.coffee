`import Ember from 'ember'`

Component = Ember.Component.extend

  didInsertElement: ->
    this.$('.modal').modal().on('hidden.bs.modal', (()->
      @sendAction('close')
    ).bind(this))


  actions:

    ok: (model)->
      @$('.modal').modal('hide')
      @sendAction('ok', model)


`export default Component`
