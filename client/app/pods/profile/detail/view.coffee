`import Ember from'ember'`

View = Ember.View.extend

  classNames: ['mc-profile']

  layoutName: 'layout/standard'


  doNothingWithIdentityCardImageListener: Ember.observer('controller.doNothingWithIdentityCardImage', ->

    if @get('controller.doNothingWithIdentityCardImage') is false

      setTimeout( (->
        el = $(this.get('element'))
        identity_card_image_file = el.find('#identity_card_image');
        identity_card_image_file.on('change', ((e) ->
          @get('controller.user').set('identity_card_image',identity_card_image_file[0].files[0]);
        ).bind(this))
      ).bind(this), 1000)
  )


  doNothingWithDriversLicenceImageListener: Ember.observer('controller.doNothingWithDriversLicenceImage', ->

    if @get('controller.doNothingWithDriversLicenceImage') is false

      setTimeout( (->
        el = $(this.get('element'))
        drivers_licence_image_file = el.find('#drivers_licence_image');
        drivers_licence_image_file.on('change', ((e) ->
          @get('controller.user').set('drivers_licence_image', drivers_licence_image_file[0].files[0]);
        ).bind(this))
      ).bind(this), 1000)
  )

`export default View`
