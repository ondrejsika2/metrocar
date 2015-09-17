`import Ember from'ember'`

View = Ember.View.extend

  classNames: ['mc-signup']

  didInsertElement: ->
    el = $(this.get('element'))

    identity_card_image_file = el.find('#identity_card_image');
    identity_card_image_file.on('change', ((e) ->
      @get('controller.user').set('identity_card_image',identity_card_image_file[0].files[0]);
    ).bind(this))

    drivers_licence_image_file = el.find('#drivers_licence_image');
    drivers_licence_image_file.on('change', ((e) ->
      @get('controller.user').set('drivers_licence_image',drivers_licence_image_file[0].files[0]);
    ).bind(this))


`export default View`
