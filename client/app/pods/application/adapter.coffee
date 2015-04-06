`import Ember from 'ember'`
`import DS from 'ember-data'`

Adapter = DS.RESTAdapter.extend

  host: 'http://local.server.metrocar.dev'
  namespace: 'api/v1'

  headers: (->
    return "Authorization": "Token " + @get("session.token")
  ).property('session.token')


#    "Authorization": (->
##      "Token 25364cf4cc9fcf7d879ecaab7be78a3cec7b9b73"
#      return 'Token ' + @get('session.token')
#    ).property('session.token')

  buildURL: ->
    url = @_super.apply(this, arguments)
    if url.charAt(url.length - 1) != '/'
      url += '/';
    return url;


`export default Adapter`

