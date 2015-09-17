`import Ember from 'ember'`


Component = Ember.Component.extend

  md5: (message) ->
    hash = CryptoJS.MD5(message);
    return hash.toString();

  tagName: 'img',

  gravatarUrl: 'https://www.gravatar.com/avatar/',

  attributeBindings: ['src'],

  src: Ember.computed('email', 'size', 'gravatarUrl', 'defaultImg', ->
    email = this.get('email') || ''

    if email.indexOf('local:') is 0
      email = email.replace('local:', '')
      return email

    email = email.replace('gravatar:', '')
    email = @md5(email)

    size = this.get('size')
    gravatarUrl = this.get('gravatarUrl')
    defaultImg = this.get('defaultImg') || 'mm'
    return gravatarUrl + email + '.jpg'
  )


`export default Component`
