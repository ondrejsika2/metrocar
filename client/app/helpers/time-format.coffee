`import Ember from 'ember'`
`import moment from 'moment'`

timeFormat = (options) ->
  date = options[0]
  format = options[1]

  if Ember.isBlank(date)
    return ''

  return moment(date).utc().format(format);

TimeFormatHelper = Ember.HTMLBars.makeBoundHelper timeFormat

`export { timeFormat }`

`export default TimeFormatHelper`
