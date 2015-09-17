`import Ember from'ember'`

View = Ember.View.extend

  classNames: ['mc-profile-success']

  layoutName: 'layout/standard'


  empty_password: Ember.observer('controller.oldPassword', ->
    if !@get('controller.oldPassword')
      @set('controller.oldPassword_errors', [@get('controller.t')('errors.empty')])
    else
      @set('controller.oldPassword_errors', [])
  )

  same_passwords: Ember.observer('controller.newPassword', 'controller.newPasswordRetry', ->
    if @get('controller.newPassword') != @get('controller.newPasswordRetry')
      @set('controller.newPasswordRetry_errors', [@get('controller.t')('errors.passportConfirmation')])
    else
      @set('controller.newPassword_errors', [])
      @set('controller.newPasswordRetry_errors', [])
  )


`export default View`
