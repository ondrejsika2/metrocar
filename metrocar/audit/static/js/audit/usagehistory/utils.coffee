define [], -> utils =

  extractCategories: (data) ->
    exclude = [
      'added'
      'event'
      'location'
      'odometer'
      'timestamp'
      'unit_id'
      'user_id'
    ]
    categories = {}
    for route in data
      for location in route.entries
        for entry in location.entries
          for field, val of entry when field not in exclude and val isnt null
            categories[field] = true
    (key for key, val of categories).sort()

  extractGraphData: (data) ->
    utils._extractGraphData data, utils.extractCategories data

  _extractGraphData: (data, categories) ->
    result = {}
    for cat in categories
      result[cat] = []
      for route in data
        routeData = []
        for location in route.entries
          for entry in location.entries
            routeData.push
              value: entry[cat] or 0
              timestamp: entry.timestamp
        result[cat].push routeData
    result

