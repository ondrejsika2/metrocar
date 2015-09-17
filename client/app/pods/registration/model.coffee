`import DS from 'ember-data'`
`import EmberValidations from 'ember-validations'`
`import LazyValidation from 'client/app/mixins/lazyvalidation'`
`import User from 'client/app/pods/user/model'`

Model = User.extend LazyValidation,

  agree: null


`export default Model`
