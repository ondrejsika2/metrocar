`import DS from 'ember-data'`

Transform = DS.Transform.extend
  serialize: (jsonData) ->
    jsonData

  deserialize: (externalData) ->
    externalData

`export default Transform`
