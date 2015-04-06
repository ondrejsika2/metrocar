`import Ember from 'ember';`
`import Base from 'simple-auth/authenticators/base'`

Authenticator = Base.extend

  userId: null,

  init: ->
    globalConfig = window.ENV['simple-auth'] || {}
    this.serverTokenEndpoint = globalConfig.serverTokenEndpoint || '/api-token-auth/'

  authenticate: (credentials) ->
    _this = this;
    return new Ember.RSVP.Promise((resolve, reject) ->
      data = {username: credentials.identification, password: credentials.password};
      _this.makeRequest(_this.serverTokenEndpoint, data).then((response) ->
        resolve(response)
      ,
        (xhr, status, error) ->
          reject(xhr.responseJSON || xhr.responseText)
      )
    )

  restore: (data) ->
    return new Ember.RSVP.Promise((resolve, reject) ->
      if !Ember.isEmpty(data.token)
        resolve(data);
      else
        reject()
    )

  invalidate: (data) ->
    success = (resolve) ->
      resolve()

    return new Ember.RSVP.Promise((resolve, reject) ->
      success(resolve);
    )

  makeRequest: (url, data) ->
    return Ember.$.ajax({
      url: url,
      type: 'POST',
      data: data,
      dataType: 'json',
      contentType: 'application/x-www-form-urlencoded'
    })


`export default Authenticator`
