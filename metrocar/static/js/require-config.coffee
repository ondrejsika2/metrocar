
requirejs.config

  baseUrl: '/static/js'

  shim:

    backbone:
      deps: ['underscore', 'jquery']
      exports: 'Backbone'

    underscore: exports: '_'

    moment: exports: 'moment'
