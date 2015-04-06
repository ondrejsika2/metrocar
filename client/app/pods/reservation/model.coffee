`import Ember from 'ember'`
`import DS from 'ember-data'`

Model = DS.Model.extend
  states:
    COMPLETED: 'completed'
    PENDING: 'pending'
    CANCELED: 'canceled'

  "cancelled": DS.attr('boolean')
  "comment": DS.attr('string')
  "created": DS.attr('date')
  "ended": DS.attr('date')
  "finished": DS.attr('boolean')
  "is_service": DS.attr('boolean')
  "modified": DS.attr('date')
  "price": DS.attr('number')
  "reserved_from": DS.attr('date')
  "reserved_until": DS.attr('date')
  "started": DS.attr('date')
  "user": DS.attr('number')
  "car": DS.belongsTo('car', async: true),


  state: Ember.computed 'finished', 'cancelled', ->
    if @get('finished')
      return @states.COMPLETED;
    else if (@get('cancelled'))
      return @.states.CANCELED;
    else
      return @states.PENDING

  is_pending: Ember.computed 'finished', 'cancelled', ->
    return !@get('finished') and !@get('cancelled')


`export default Model`
