`import Ember from 'ember'`

Route = Ember.Route.extend

  queryParams:
    page:
      refreshModel: true

  model: (params)->

    query = {};

    if(Ember.isPresent(params.page))
      query.page = params.page;

    return @store.find('fuelbill', query)


  setupController: (ctrl, model) ->
    ctrl.set('fuelbills', model)
    ctrl.set('totalPages', model.get('meta.pages'));

`export default Route`
