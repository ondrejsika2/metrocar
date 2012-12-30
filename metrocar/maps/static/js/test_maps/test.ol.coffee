define [
  'jquery'
  'tests/chai',
  'maps/ol'
], ($, {assert, should}, ol) ->

  should()

  describe 'maps', ->

    describe 'ol (OpenLayers)', ->

      olMap = ol.createMap $('<div/>')[0]
      for f in [
        'onMoved'
        'getBounds'
        'setBounds'
        'drawRoute'
        'drawMarker'
        'drawIconMarker'
        'drawMarkers'
        'clear'
        'focus'
      ]
        it "should support #{f}", -> (typeof olMap[f]).should.equal 'function'
