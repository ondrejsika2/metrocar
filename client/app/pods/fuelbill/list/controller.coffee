`import Ember from 'ember'`


Controller = Ember.ArrayController.extend

  sortProperties: ['datetime:desc'],
  fuelbillsSorted: Ember.computed.sort('fuelbills', 'sortProperties'),

  queryParams: [
    'page',
  ],

  page: 1,

  totalPages: null,

  prevPage: Ember.computed('page', ->
    return this.get('page') - 1;
  )

  nextPage: Ember.computed('page', ->
    return this.get('page') + 1;
  )

  isFirstPage: Ember.computed('page', ->
    return this.get('page') == 1;
  )

  isLastPage: Ember.computed('page', 'totalPages', ->
    return this.get('page') >= this.get('totalPages');
  )

  pageRange: Ember.computed('totalPages', ->
    result = Ember.A();

    i = 1
    while i <= @get('totalPages')
      result.push i
      i++

    return result;
  )




`export default Controller`
