requirejs [
  'jquery'
  'cars/views'
], ($, {CarMap}) -> new CarMap el: $('#app')[0]
