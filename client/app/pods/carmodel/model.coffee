`import DS from 'ember-data'`

Model = DS.Model.extend

  name: DS.attr('string')
  manufacturer: DS.attr('number')
  type: DS.attr('number')
  engine: DS.attr('string')
  seats_count: DS.attr('number')
  storage_capacity: DS.attr('number')
  main_fuel: DS.attr('number')
  alternative_fuel: DS.attr('number')
  notes: DS.attr('string')
  image: DS.attr('number')

  cars: DS.hasMany('car')


`export default Model`
