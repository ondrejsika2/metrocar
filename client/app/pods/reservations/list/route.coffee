`import Ember from 'ember';`
`import AuthenticatedRouteMixin from 'simple-auth/mixins/authenticated-route-mixin'`


Route = Ember.Route.extend AuthenticatedRouteMixin,

  queryParams:
    page:
      refreshModel: true

  model: (params)->

    query = {}

    if(Ember.isPresent(params.page))
      query.page = params.page;

    return @store.find('reservation', query)

  afterModel: (model) ->
    modelId = model.get('id');

    return @get('store').find('car', reservation: modelId)
      .then(((cars) ->
        return @get('store').find('parking', id: cars.get('id'))
      ).bind(this))

  setupController: (ctrl, model) ->
    this._super.apply(this, arguments)

    ctrl.set('reservations', model)
    ctrl.set('totalPages', model.get('meta.pages'))




`export default Route`

