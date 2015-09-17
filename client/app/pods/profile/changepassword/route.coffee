`import Ember from 'ember'`

Route = Ember.Route.extend

  setupController: (ctrl, model) ->
    ctrl.set('oldPassword', '')
    ctrl.set('newPassword', '')
    ctrl.set('newPasswordRetry', '')
    ctrl.set('oldPassword_errors', [])


`export default Route`
