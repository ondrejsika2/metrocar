define [
  'backbone'
], (Backbone) ->

  class Select extends Backbone.View
    ###
    Expected to be created with el: some element containing a single <select>
    ###

    events:
      'change select': 'changed'

    changed: -> @trigger 'change', @getValue()

    getValue: -> if val = @$('select').val() then val else null

    setValue: (value) ->
      @$('select').val value
      @changed()
