from djangosanetesting.cases import UnitTestCase

from metrocar.utils.geotrack_queries import usage_history


class TestUsageHistory(UnitTestCase):

    def test_prune_journeys_to(self):
        journeys = [
            {'entries': [0, 1, 2, 3, 4, 5, 6, 7], 'events': 'journey1-events'},
            {'entries': range(15), 'events': 'journey2-events'},
            {'entries': [0, 1, 2], 'events': 'journey3-events'},
        ]

        result = list(usage_history.prune_journeys_to(10, journeys))

        self.assert_equals(result, [
            {'entries': [0, 3, 7], 'events': 'journey1-events'},
            {'entries': [0, 3, 5, 8, 10, 14], 'events': 'journey2-events'},
            {'entries': [0, 2], 'events': 'journey3-events'},
        ])

    def test_group_by_location(self):
        entries = [
            {'location': (12, 34), 'event': 'E1'},
            {'location': (12, 34), 'event': 'E2'},
            {'location': (12, 34), 'event': 'E3'},
            {'location': (13, 34), 'event': 'E4'},
            {'location': (14, 34), 'event': 'E5'},
            {'location': (15, 34), 'event': 'E6'},
            {'location': (16, 34), 'event': 'E7'},
            {'location': (16, 34), 'event': 'E8'},
            {'location': (17, 34), 'event': 'E9'},
        ]
        result = list(usage_history.group_by_location(entries))

        self.assert_equals(result, [
            {'location': (12, 34), 'entries': (
                {'location': (12, 34), 'event': 'E1'},
                {'location': (12, 34), 'event': 'E2'},
                {'location': (12, 34), 'event': 'E3'},
            )},
            {'location': (13, 34), 'entries': (
                {'location': (13, 34), 'event': 'E4'},
            )},
            {'location': (14, 34), 'entries': (
                {'location': (14, 34), 'event': 'E5'},
            )},
            {'location': (15, 34), 'entries': (
                {'location': (15, 34), 'event': 'E6'},
            )},
            {'location': (16, 34), 'entries': (
                {'location': (16, 34), 'event': 'E7'},
                {'location': (16, 34), 'event': 'E8'},
            )},
            {'location': (17, 34), 'entries': (
                {'location': (17, 34), 'event': 'E9'},
            )},
        ])
