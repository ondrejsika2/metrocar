`import Ember from 'ember'`

timeAgo = (date) ->
  return moment(date[0]).fromNow()

TimeAgoHelper = Ember.HTMLBars.makeBoundHelper timeAgo

`export { timeAgo }`

`export default TimeAgoHelper`
