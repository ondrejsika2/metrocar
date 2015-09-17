`import DS from 'ember-data'`
`import LazyValidation from 'client/app/mixins/lazyvalidation'`
`import User from 'client/app/pods/user/model'`

Model = User.extend( LazyValidation,)



`export default Model`
