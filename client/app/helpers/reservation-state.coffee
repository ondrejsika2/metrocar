`import Ember from 'ember'`
`import Reservation from 'client/app/pods/reservation/model'`

reservationState = (state) ->
  switch state[0]
    when Reservation.proto().states.COMPLETED then return new Ember.Handlebars.SafeString('<i class="fa fa-check mc-icon-state"></i>')
    when Reservation.proto().states.PENDING then return new Ember.Handlebars.SafeString('<i class="fa fa-clock-o mc-icon-state"></i>')
    when Reservation.proto().states.CANCELED then return new Ember.Handlebars.SafeString('<i class="fa fa-times mc-icon-state"></i>')
    else return null

ReservationStateHelper = Ember.HTMLBars.makeBoundHelper reservationState

`export { reservationState }`

`export default ReservationStateHelper`
