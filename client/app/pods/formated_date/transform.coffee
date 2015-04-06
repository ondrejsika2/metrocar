`import DS from 'ember-data'`

Transform = DS.Transform.extend

  deserialize: (serialized) ->
    return serialized

  serialize: (deserialized) ->
    return deserialized.format('YYYY-MM-DD')

`export default Transform`

