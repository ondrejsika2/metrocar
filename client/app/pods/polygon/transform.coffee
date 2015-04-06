`import DS from 'ember-data'`

Transform = DS.Transform.extend

  deserialize: (serialized) ->
    preResult = serialized.replace('POLYGON ((','')
    preResult = preResult.replace('))','')
    preResult = preResult.split(', ')

    finalResult = []
    preResult.forEach((coordinate)->
      finalResult.push(coordinate.split(' '))
    )

    return finalResult

  serialize: (deserialized) ->
    return deserialized

`export default Transform`

