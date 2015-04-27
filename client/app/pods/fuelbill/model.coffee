`import DS from 'ember-data'`
`import LazyValidation from 'client/app/mixins/lazyvalidation'`

Model = DS.Model.extend LazyValidation,

  validations:
    money_amount:
      presence: true
    car:
      presence: true
    fuel:
      presence: true
    liter_count:
      presence: true


  FUEL_TYPES:
    1: "Diesel"
    2: "Natural"

  account: DS.attr('number')
  money_amount: DS.attr('number')
  fuel: DS.attr('number')
  liter_count: DS.attr('number')
  place: DS.attr('string')
  image: DS.attr('file')
  approved: DS.attr('boolean')
  datetime: DS.attr('date')

  car: DS.belongsTo('car', async: true),

  fuel_name: (->
    @get('FUEL_TYPES')[@get('fuel')]
  ).property('fuel')


`export default Model`
