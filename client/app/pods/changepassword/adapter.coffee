`import ApplicationAdapter from '../application/adapter'`
`import FormDataAdapterMixin from '../../mixins/form-data-adapter'`

FormDataAdapter = ApplicationAdapter.extend( FormDataAdapterMixin,

  isNecessary: (field, value)->

    if field is 'drivers_licence_image' and typeof value is "string"
      return false

    if field is 'identity_card_image' and typeof value is "string"
      return false

    return true

)

`export default FormDataAdapter`
