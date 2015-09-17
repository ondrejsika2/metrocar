`import Ember from'ember'`

View = Ember.View.extend

  classNames: ['account-activity-timeline']

  layoutName: 'layout/standard'

  didInsertElement: ->
    @$().bind('inview', ((event, isInView, visiblePartX, visiblePartY) ->
      if isInView
        Ember.tryInvoke(@get('controller'), 'loadMore')
    ).bind(this))

`export default View`
