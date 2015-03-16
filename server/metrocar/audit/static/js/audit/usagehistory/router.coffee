define ['backbone'], (Backbone) ->

  class Router extends Backbone.Router

    routes:
      'q/*query': 'query'

    query: (args...) -> # we'll just use the router to emit events
