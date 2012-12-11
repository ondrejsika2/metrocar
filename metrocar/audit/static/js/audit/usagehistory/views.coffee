define [
  'module'
  'underscore'
  'backbone'
  'jquery'
  'moment'
  'maps/ol'
  'maps/utils'
  'audit/usagehistory/router'
  'jquery-ui'
], (module, _, Backbone, $, moment, OLMap, utils, Router) ->

  config = module.config()

  {boundsToPolygon, polygonToBounds} = utils

  encodeQuery = (object) -> encodeURIComponent JSON.stringify object
  decodeQuery = (string) -> JSON.parse decodeURIComponent string

  enlargeBounds = ({left, right, top, bottom}) ->
    # Make bounds a bit larger so the displayed route doesn't seem cut-off
    left: left - 0.01
    right: right + 0.01
    top: top + 0.01
    bottom: bottom - 0.01


  class UnitSelect extends Backbone.View

    events:
      'change select': 'changed'

    changed: -> @trigger 'change', @getValue()

    getValue: -> if val = @$('select').val() then [val] else null

    setValue: (value) ->
      @$('select').val value
      @changed()


  class Calendar extends Backbone.View

    events:
      'change input': 'changed'

    initialize: ->
      @input = @$('input')
      console.log @input
      # @input.datepicker onSelect: =>
      #   @input.val @input.datepicker('getDate')?.toISOString() or ''
      #   @changed()

    changed: -> @trigger 'change'

    getValue: -> @input.val()

    setValue: -> #TODO


  marker = (data) ->
    exclude = ['unit_id']
    tables = for entry in data.entries
      rows = (for k, v of entry when (v and k not in exclude)
        "<tr><th>#{k}</th><td>#{v}</td></tr>").join '\n'
      "<table><tbody>#{rows}</tbody></table>"

    location: data.location
    # content: "#{data.location}<br>#{data.timestamp}"
    content: tables.join '<br>'


  class Map extends Backbone.View

    initialize: ->
      @map = OLMap @el
      @map.onMoved (bounds) => @trigger 'change', boundsToPolygon bounds

    getValue: -> boundsToPolygon enlargeBounds @map.getBounds()

    setValue: (polygon) -> @map.setBounds polygonToBounds polygon

    display: (data) ->
      @map.clear()
      if data then for route in data
        console.log 'route': route
        @map.drawRoute route.entries.map (x) -> x.location
        @map.drawMarkers route.entries.map marker


  # exports
  App: class App extends Backbone.View

    initialize: ->
      @map = new Map el: @$('.map')

      @controls =
        units: (new UnitSelect el: @$('.unit-select'))
        start: (new Calendar el: @$('.start-cal'))
        end: (new Calendar el: @$('.end-cal'))
        in_polygon: @map

      @setupRouter()

      for name, widget of @controls
        do (name, widget) => widget.on 'change', => @processCurrentSettings()

      @processCurrentSettings()

      @requestId = 0
      @latestResponse = 0

    processCurrentSettings: ->
      query = @constructQuery()
      # only do something if a unit is selected
      if query.units
        @router.navigate "q/#{encodeQuery query}", replace: true
        @queryServer _.extend query, request_id: @requestId += 1

    constructQuery: ->
      q = {}
      (q[name] = widget.getValue()) for name, widget of @controls
      q

    queryServer: (query) ->
      $.ajax
        url: config.queryUrl
        type: 'POST'
        data: JSON.stringify query
        success: (response) =>
          if response.request_id > @latestResponse
            @latestResponse = response.request_id
            @display response
        error: (args...) -> console.log 'AJAX error', args...

    display: (response) ->
      console.log 'display', response
      @map.display response.results

    setupRouter: ->
      @router = new Router

      @router.on 'route:query', (querystring) =>
        q = decodeQuery querystring
        for name, val of q when val
          @controls[name].setValue val

      Backbone.history.start
        pushState: true
        root: config.rootUrl
