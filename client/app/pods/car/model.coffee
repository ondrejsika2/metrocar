`import Ember from 'ember'`
`import DS from 'ember-data'`

Model = DS.Model.extend

  active: DS.attr('boolean')
  dedicated_parking_only: DS.attr('boolean')
  manufacture_date: DS.attr('date')
  registration_number: DS.attr('string')
  image: DS.attr('string')
  model: DS.belongsTo('carmodel', async: true)
  color: DS.belongsTo('carcolor', async: true)
  owner: DS.attr('number')
  home_subsidiary: DS.attr('number')
  last_echo: DS.attr('date')
  _last_position: DS.attr()
  _last_address: DS.attr('string')

  parking: DS.belongsTo('parking', async: true),

  reservations: DS.hasMany('reservation')

  car_name: DS.attr('string')

`export default Model`
