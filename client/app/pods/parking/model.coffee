`import DS from 'ember-data'`

Parking = DS.Model.extend

  name: DS.attr('string')
  places_count: DS.attr('number')
  land_registry_number: DS.attr('string')
  street: DS.attr('string')
  city: DS.attr('string')
  polygon: DS.attr('polygon')
  reservations: DS.hasMany('car')


`export default Parking`
