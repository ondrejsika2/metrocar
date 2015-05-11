`import Ember from 'ember'`
`import moment from 'moment'`

timeAgoInWords = (options) ->
  date = options[0]

  if Ember.isBlank(date)
    return ''

  return moment(date).add(moment.parseZone(date).zone(), 'minutes').fromNow()

TimeAgoInWordsHelper = Ember.HTMLBars.makeBoundHelper timeAgoInWords

`export { timeAgoInWords }`

`export default TimeAgoInWordsHelper`
