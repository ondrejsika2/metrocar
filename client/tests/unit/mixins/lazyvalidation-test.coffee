`import Ember from 'ember'`
`import LazyvalidationMixin from '../../../mixins/lazyvalidation'`
`import { module, test } from 'qunit'`

module 'LazyvalidationMixin'

# Replace this with your real tests.
test 'it works', (assert) ->
  LazyvalidationObject = Ember.Object.extend LazyvalidationMixin
  subject = LazyvalidationObject.create()
  assert.ok subject
