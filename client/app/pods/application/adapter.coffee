`import Ember from 'ember'`
`import DS from 'ember-data'`

Adapter = DS.RESTAdapter.extend

  host: window.ENV['metrocarServer']
  namespace: 'api/v1'

  headers: (->
    return "Authorization": "Token " + @get("session.token")
  ).property('session.token')


  buildURL: ->
    url = @_super.apply(this, arguments)
    if url.charAt(url.length - 1) != '/'
      url += '/';
    return url;


`export default Adapter`

