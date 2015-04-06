`import DS from 'ember-data'`

Model = DS.Model.extend

  username: DS.attr('string')
  first_name: DS.attr('string')
  last_name: DS.attr('string')
  email: DS.attr('string')
  is_active: DS.attr('boolean')
  date_of_birth: DS.attr('formated_date')
  drivers_licence_number: DS.attr('string')
  gender: DS.attr('string')
  identity_card_number: DS.attr('string')
  primary_phone: DS.attr('string')
  language: DS.attr('string')

`export default Model`
