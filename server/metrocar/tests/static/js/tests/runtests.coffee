requirejs.config shim: 'tests/mocha': exports: 'mocha'

requirejs [
  'tests/chai'
  'tests/mocha'
], (chai, mocha) ->

  mocha.setup 'bdd'

  requirejs [
    'audit/test_usagehistory/test.utils'
    'test_maps/test.ol'
  ], -> mocha.run()
