`import Ember from 'ember'`

Controller = Ember.Controller.extend

  actions:
    cancelReservation: () ->
      reservation = @get('model')
      reservation.deleteRecord();
      reservation.save()




`export default Controller`
