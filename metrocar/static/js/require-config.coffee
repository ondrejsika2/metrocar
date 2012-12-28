
requirejs.config

  baseUrl: '/static/js'

  paths:
    d3: 'd3.v3.min'

  shim:

    jquery: exports: '$'

    underscore: exports: '_'

    moment: exports: 'moment'

    d3: exports: 'd3'

    backbone:
      deps: ['underscore', 'jquery']
      exports: 'Backbone'

    coffeekup:
      deps: ['coffee-script']
      exports: 'CoffeeKup'

    rickshaw:
      deps: ['d3']
      exports: 'Rickshaw'

    'jquery-ui':
      deps: ['jquery']
