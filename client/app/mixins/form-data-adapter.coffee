`import Ember from 'ember'`

Mixin = Ember.Mixin.create

# Overwrite to change the request types on which Form Data is sent
  formDataTypes: ['POST', 'PUT', 'PATCH'],

  isNecessary: (field, value) ->
    return true

  ajaxOptions: (url, type, options) ->

    data = null

    if (options and options.hasOwnProperty('data'))
      data = options.data

    hash = @_super.apply(this, arguments)

    if (typeof FormData isnt undefined and data and @formDataTypes.contains(type))

      formData = new FormData()

      Ember.keys(data).forEach( ((key) ->
        if (typeof data[key] isnt undefined and @isNecessary(key, data[key]))
          formData.append(key, data[key])
      ).bind(this))

      hash.processData = false
      hash.contentType = false
      hash.data = formData

    return hash;

`export default Mixin`
