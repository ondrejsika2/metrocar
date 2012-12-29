define [
  'tests/chai',
  'audit/usagehistory/utils'
], ({assert, should}, utils) ->

  should()

  routeData = [
    # data can contain multiple routes
    {
      # route 1
      events: []
      entries: [
        # entries contain entries grouped by location
        {
          location: [1, 2]
          entries: [
            # list of entries in given location
            {
              location: [1, 2]
              timestamp: '1234'
              added: '45468'
              unit_id: 1234
              user_id: 123
              velocity: 1
              consumption: 12
            },
            {
              location: [1, 2]
              timestamp: '12345'
              unit_id: 1234
              user_id: 123
              velocity: 2
              throttle: 20
            },
          ],
        },
        {
          location: [2, 3]
          entries: [
            {
              consumption: 12.5
              velocity: 3
              timestamp: '123456'
            }
          ]
        }
      ]
    },
    {
      # route 2
      events: []
      entries: [
        {
          location: [2, 3]
          entries: [
            {
              location: [1, 2]
              timestamp: '1234'
              unit_id: 1234
              user_id: 123
              velocity: 1.4
              event: 'CRASH'
              fuel_remaining: 31.2
            }
          ]
        }
      ]
    },
  ]


  describe 'utils', ->

    describe 'extractCategories', ->
      it 'should extract graphable categories from route-data', ->

        categories = utils.extractCategories(routeData).sort()

        categories.should.deep.equal [
          'consumption'
          'fuel_remaining'
          'throttle'
          'velocity'
        ]

    describe '_extractGraphData', ->
      it 'should restructure route-data to a format suitable for graphing', ->

        result = utils._extractGraphData routeData, ['velocity']

        result.should.deep.equal {
          velocity: [
            [
              {value: 1, timestamp: '1234'}
              {value: 2, timestamp: '12345'}
              {value: 3, timestamp: '123456'}
            ],
            [
              {value: 1.4, timestamp: '1234'}
            ]
          ]
        }
