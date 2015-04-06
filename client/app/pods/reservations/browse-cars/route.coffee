`import Ember from 'ember'`

Route = Ember.Route.extend

  model: ->
    return Ember.A([
      {title: "Škoda Octavia Modrá", lat: 50.080408, lng: 14.414197},
      {title: "Škoda Fabia Zelená", lat: 50.036262, lng: 14.518328},
      {title: "Škoda Yeti Žlutá", lat: 50.106260, lng: 14.567323}
    ]);


`export default Route`
