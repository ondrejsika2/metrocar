`import Ember from 'ember'`
`import AccountActivity from 'client/app/pods/accountactivity/model'`

accountActivityType = (type) ->
  switch type[0]
    when AccountActivity.proto().TYPES.FUEL_BILL then return new Ember.Handlebars.SafeString('<i class="fa fa-clock-o mc-icon-state"></i>')
    when AccountActivity.proto().TYPES.RESERVATION_BILL then return new Ember.Handlebars.SafeString('<i class="fa fa-road mc-icon-state"></i>')
    when AccountActivity.proto().TYPES.DEPOSIT then return new Ember.Handlebars.SafeString('<i class="fa fa-money mc-icon-state"></i>')
    else return null

AccountActivityTypeHelper = Ember.HTMLBars.makeBoundHelper accountActivityType

`export { accountActivityType }`

`export default AccountActivityTypeHelper`
