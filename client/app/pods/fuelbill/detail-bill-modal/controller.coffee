`import Ember from 'ember'`

Controller = Ember.Controller.extend(

  url: (->
    return window.ENV['metrocarServer'] + '/files/' + @get('model');
  ).property('model')

)


`export default Controller`
