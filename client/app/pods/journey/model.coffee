`import DS from 'ember-data'`

Model = DS.Model.extend

  comment: DS.attr('string')
  start_datetime: DS.attr('date')
  end_datetime: DS.attr('date')
  length: DS.attr('string')
  total_price: DS.attr('string')
  type: DS.attr('string')
  speedometer_start: DS.attr('number')
  speedometer_end: DS.attr('number')

  reservation: DS.belongsTo('reservation', async: true)
  car: DS.belongsTo('car', async: true)
  user: DS.belongsTo('user', async: true)


`export default Model`
