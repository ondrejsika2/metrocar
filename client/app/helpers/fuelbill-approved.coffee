`import Ember from 'ember'`
`import Reservation from 'client/app/pods/reservation/model'`

fuelbillApproved = (approved) ->
  if approved[0]
    return new Ember.Handlebars.SafeString('<i class="fa fa-check mc-icon-state"></i>')
  else
    return new Ember.Handlebars.SafeString('<i class="fa fa-clock-o mc-icon-state"></i>')

FuelbillApprovedHelper = Ember.HTMLBars.makeBoundHelper fuelbillApproved

`export { fuelbillApproved }`

`export default FuelbillApprovedHelper`
