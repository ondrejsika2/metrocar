`import DS from 'ember-data'`
`import EmberValidations from 'ember-validations'`
`import LazyValidation from 'client/app/mixins/lazyvalidation'`

Model = DS.Model.extend LazyValidation,

  validations:
    first_name:
      presence: true
    last_name:
      presence: true
    email:
      inline: EmberValidations.validator( ->
        re = /\S+@\S+\.\S+/;
        if re.test(@model.get('email')) is false
          t = this.model.container.lookup('utils:t')
          return t('errors.email')
      )
    username:
      presence: true
    date_of_birth:
      presence: true
    drivers_licence_number:
      presence: true
    identity_card_number:
      presence: true
    primary_phone:
      presence: true
      inline: EmberValidations.validator( ->
        re = /^[1-9][0-9]{2} ?[0-9]{3} ?[0-9]{3}$/;
        if re.test(@model.get('primary_phone')) is false
          t = this.model.container.lookup('utils:t')
          return t('errors.phone')
      )
    password:
      presence: true
      inline: EmberValidations.validator(->
        if !@model.get('password')
          return
        if !@model.get('retry_password')
          return
        if @model.get('password') == @model.get('retry_password')
          @model.set('errors.password', [])
          @model.set('errors.retry_password', [])
          return

        @model.set('errors.retry_password', ["Zadaná hesla musí být stejná"])
        return
      )
    retry_password:
      presence: true
      inline: EmberValidations.validator(->
        if !@model.get('password')
          return
        if !@model.get('retry_password')
          return
        if @model.get('password') == @model.get('retry_password')
          @model.set('errors.password', [])
          @model.set('errors.retry_password', [])
          return

        return "Zadaná hesla musí být stejná"
      )
    drivers_licence_image:
      presence: true
    identity_card_image:
      presence: true


  first_name: DS.attr('string')
  last_name: DS.attr('string')
  email: DS.attr('string')
  username: DS.attr('string')
  active: DS.attr('boolean')
  date_of_birth: DS.attr('formated_date')
  drivers_licence_number: DS.attr('string')
  identity_card_number: DS.attr('string')
  primary_phone: DS.attr('string')
  password: DS.attr('string')
  retry_password: null
  drivers_licence_image: DS.attr('file')
  identity_card_image: DS.attr('file')


`export default Model`
