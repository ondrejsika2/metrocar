`import Ember from 'ember'`

isEven = (index) ->
  return (index % 2) == 0

IsEvenHelper = Ember.HTMLBars.makeBoundHelper isEven

`export { isEven }`

`export default IsEvenHelper`
