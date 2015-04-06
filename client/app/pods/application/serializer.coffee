`import DS from 'ember-data'`

Serializer = DS.RESTSerializer.extend

  extractArray: (store, type, payload) ->
    payloadTemp = {}
    payloadTemp[type.typeKey] = payload
    return @_super(store, type, payloadTemp)


  extractSingle: (store, type, payload, id) ->
    payloadTemp = {}
    payloadTemp[type.typeKey] = [payload]
    return @_super(store, type, payloadTemp, id)


  serializeIntoHash: (data, type, record, options) ->
    properties = @serialize(record, options)
    for key,val of properties
      data[key] = val


`export default Serializer`
