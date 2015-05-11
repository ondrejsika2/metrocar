`import Ember from'ember'`

View = Ember.View.extend

  classNames: ['mc-profile']

  layoutName: 'layout/standard'

  didInsertElement: ->
    el = $(this.get('element'))

    fileField = el.find('#file-field');
    fileField.on('change', ((e) ->
      @get('controller.fuelBill').set('image',fileField[0].files[0]);
    ).bind(this))

`export default View`
