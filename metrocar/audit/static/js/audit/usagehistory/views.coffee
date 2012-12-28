define [
  'module'
  'underscore'
  'backbone'
  'jquery'
  'moment'
  'rickshaw'
  'maps/ol'
  'maps/utils'
  'audit/usagehistory/router'
  'audit/usagehistory/templates'
  'audit/usagehistory/utils'
  'common/views/map'
  'jquery-ui'
], (module, _, Backbone, $, moment, Rickshaw, OLMap, map_utils, Router, templates, utils, MapView) ->

  console.log 'graphsetTpl', templates.graphRow
  console.log templates.graphRow caption: 'hellp'

  config = module.config()

  {boundsToPolygon, polygonToBounds} = map_utils
  {extractGraphData} = utils

  encodeQuery = (object) -> encodeURIComponent JSON.stringify object
  decodeQuery = (string) -> JSON.parse decodeURIComponent string


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
      @input.datepicker onSelect: =>
        @input.val @input.datepicker('getDate')?.toISOString() or ''
        @changed()

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
    content: tables.join '<br>'


  class Map extends MapView

    display: (data) ->
      @map.clear()
      if data then for route in data
        @map.drawRoute route.entries.map (x) -> x.location
        @map.drawMarkers route.entries.map marker


  timeToInt = (timestamp) -> moment(timestamp).unix()


  class GraphSet extends Backbone.View

    events:
      'click .graph-row .header': 'toggleCollapse'

    initialize: ->
      @collapsed = {}

    display: (data) ->
      console.log 'GraphSet display', data
      @$el.html ''
      palette = new Rickshaw.Color.Palette
      for category, cData of data
        graphRow = new GraphRow
          collapsed: @collapsed[category]
          category: category
          color: palette.color()
          width: 1200
        @$el.append graphRow.$el.addClass 'graph-row-wrapper'
        graphRow.render cData

    toggleCollapse: ({target}) =>
      row = $(target).closest '.graph-row-wrapper'
      category = row.find('.header .caption').text()
      if row.is '.collapsed'
        @collapsed[category] = false
        row.removeClass 'collapsed'
      else
        @collapsed[category] = true
        row.addClass 'collapsed'


  class GraphRow extends Backbone.View

    initialize: ({@category, @collapsed}) ->
      console.log 'initialized GraphRow for', @category

    render: (data) ->
      @$el.html templates.graphRow caption: @category
      if @collapsed then $(@el).addClass 'collapsed'

      totalCount = data.map((x) -> x.length).reduce (a, b) -> a + b

      for dataset in data
        (new Graph
          el: $('<div>').appendTo(@$('.content'))[0]
          category: @category
          width: @options.width * (dataset.length / totalCount)
          color: @options.color
        ).render dataset


  class Graph extends Backbone.View

    initialize: ({@category}) ->
      console.log 'initialized Graph', @category

    render: (data) ->
      padding = 20
      args =
        element: @el
        width: @options.width - padding
        height: 150
        renderer: 'line'
        series: [
          name: @category
          data: @processValues data
          color: @options.color
        ]
      @graph = new Rickshaw.Graph args

      if @options.width > 250
        new Rickshaw.Graph.Axis.Time graph: @graph

      new Rickshaw.Graph.HoverDetail graph: @graph

      @graph.render()

    processValues: (values) ->
      for {value, timestamp} in values
        x: timeToInt timestamp
        y: value


  class App extends Backbone.View

    initialize: ->
      @map = new Map el: @$('.map'), MapModule: OLMap
      @graphSet = new GraphSet el: @$('.graphs')

      @controls =
        units: (new UnitSelect el: @$('.unit-select'))
        start: (new Calendar el: @$('.start-cal'))
        end: (new Calendar el: @$('.end-cal'))
        in_polygon: @map

      @setupRouter()

      for name, widget of @controls
        do (name, widget) => widget.on 'change', => @processCurrentSettings()

      @requestId = 0
      @latestResponse = 0

      @processCurrentSettings()

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
      @map.display response.results
      @graphSet.display extractGraphData response.results

    setupRouter: ->
      @router = new Router

      @router.on 'route:query', (querystring) =>
        q = decodeQuery querystring
        for name, val of q when val
          @controls[name].setValue val

      Backbone.history.start
        pushState: true
        root: config.rootUrl


  # exports:
  {App}
