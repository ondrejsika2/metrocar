`import Ember from 'ember'`
`import DS from 'ember-data'`
`import EmberValidations from 'ember-validations'`
`import LazyValidation from 'client/app/mixins/lazyvalidation'`

Model = DS.Model.extend LazyValidation,

  validations:
    reserved_from:
      presence: true
    reserved_until:
      presence: true
    car:
      presence: true
      inline: EmberValidations.validator( ->
        if not @get('model.car.content')
          t = this.model.container.lookup('utils:t')
          return t('errors.blank')
      )
    parking:
      presence: true

  states:
    COMPLETED: 'completed'
    PENDING: 'pending'
    CANCELED: 'canceled'

  cancelled: DS.attr('boolean')
  comment: DS.attr('string')
  created: DS.attr('date')
  ended: DS.attr('date')
  finished: DS.attr('boolean')
  is_service: DS.attr('boolean')
  modified: DS.attr('date')
  price: DS.attr('number')
  reserved_from: DS.attr('date')
  reserved_until: DS.attr('date')
  started: DS.attr('date')
  user: DS.attr('number')

  car: DS.belongsTo('car', async: true)

  journeys: DS.hasMany('journey')

  parking:null


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
