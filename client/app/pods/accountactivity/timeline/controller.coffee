`import Ember from 'ember'`

Controller = Ember.ArrayController.extend

  sortProperties: ['datetime:desc'],
  accountactivitiesSorted: Ember.computed.sort('accountactivities', 'sortProperties'),

  currentPage: 1,

  canLoadMore: Ember.computed('currentPage', 'totalPages', ->
    return @get('currentPage') < @get('totalPages')
  )

  actions:
    loadMore: ->
      if this.get('canLoadMore')
        @set('isLoading', true)
        page = @incrementProperty('currentPage')
        @get('store').findQuery('accountactivity', {page: page})
        .then(((accountActivities) ->
          @get('accountactivities').pushObjects(accountActivities.get('content'))
          @set('isLoading', false)
        ).bind(this))
      else
        @set('isLoading', true)


`export default Controller`
