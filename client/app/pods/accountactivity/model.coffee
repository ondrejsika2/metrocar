`import DS from 'ember-data'`

Model = DS.Model.extend

  TYPES:
    RESERVATION_BILL: 'ReservationBill'
    DEPOSIT: 'Deposit'
    FUEL_BILL: 'FuelBill'

  datetime: DS.attr('date')
  money_amount: DS.attr('number')
  activity_type: DS.attr('string')

  componentName: (->
    switch @get('activity_type')
      when @get('TYPES.FUEL_BILL') then return 'accountactivity/timeline/fuelbill-activity'
      when @get('TYPES.RESERVATION_BILL') then return 'accountactivity/timeline/reservationbill-activity'
      when @get('TYPES.DEPOSIT') then return 'accountactivity/timeline/deposit-activity'
      else return null
  ).property('activity_type')


`export default Model`
