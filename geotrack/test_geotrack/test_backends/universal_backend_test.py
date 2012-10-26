from datetime import datetime
from functools import partial

from testing_project.utils import entry


class BackendTest:

    backend = None

    maxDiff = None

    def test_store_and_retrieve(self):
        # store some log entries
        self.backend.store(
            unit_id=321,
            timestamp=datetime(2012, 12, 12, 12, 12, 12),
            location=(10, 20),
            added=datetime(2012, 12, 12, 12, 12, 13),
            custom_field=42,
        )

        self.backend.store(
            unit_id=321,
            timestamp=datetime(2012, 12, 12, 12, 12, 14),
            location=(10, 20.1),
            added=datetime(2012, 12, 12, 12, 12, 15),
            custom_field=43,
        )

        # retrieve all
        native_results = self.backend.query()

        # transform to universal representation
        results = self.backend.transform(native_results)

        # check contents
        self.assertEqual(results, (
            dict(
                unit_id=321,
                timestamp=datetime(2012, 12, 12, 12, 12, 12),
                location=(10, 20),
                added=datetime(2012, 12, 12, 12, 12, 13),
                custom_field=42,
            ),
            dict(
                unit_id=321,
                timestamp=datetime(2012, 12, 12, 12, 12, 14),
                location=(10, 20.1),
                added=datetime(2012, 12, 12, 12, 12, 15),
                custom_field=43,
            )
        ))

    def test_filter_location(self):
        self.backend.store(**entry(location=(50.07653, 14.43398)))
        self.backend.store(**entry(location=(49.00905, 17.18262)))
        self.backend.store(**entry(location=(49.39668, 13.24951)))
        self.backend.store(**entry(location=(46.84516, 0.85693)))
        native_results = self.backend.query(in_polygon=(
            (51.65893, 14.76563),
            (47.79840, 10.70068),
            (48.45835, 21.48926),
            (51.65893, 14.76563),
        ))
        results = self.backend.transform(native_results)
        locations = set([r['location'] for r in results])
        self.assertEqual(locations, set([
            (50.07653, 14.43398),
            (49.00905, 17.18262),
            (49.39668, 13.24951),
        ]))

    def test_filter_time(self):
        self.backend.store(**entry(timestamp=datetime(2012, 1, 1)))
        self.backend.store(**entry(timestamp=datetime(2012, 1, 2)))
        self.backend.store(**entry(timestamp=datetime(2012, 1, 3)))
        self.backend.store(**entry(timestamp=datetime(2012, 1, 4)))
        self.backend.store(**entry(timestamp=datetime(2012, 1, 5)))
        native_results = self.backend.query(
            start=datetime(2012, 1, 2), end=datetime(2012, 1, 4))
        results = self.backend.transform(native_results)
        times = [r['timestamp'] for r in results]
        self.assertEqual(times, [
            datetime(2012, 1, 2),
            datetime(2012, 1, 3),
            datetime(2012, 1, 4),
        ])

    def test_filter_units(self):
        self.backend.store(**entry(unit_id=2))
        self.backend.store(**entry(unit_id=2))
        self.backend.store(**entry(unit_id=3))
        self.backend.store(**entry(unit_id=4))
        self.backend.store(**entry(unit_id=5))
        native_results = self.backend.query(units=[2, 3])
        results = self.backend.transform(native_results)
        units = sorted([r['unit_id'] for r in results])
        self.assertEqual(units, [2, 2, 3])

    def test_last_known_position(self):
        t = partial(datetime, 2012, 1, 1)
        store = lambda **kw: self.backend.store(**entry(**kw))
        store(unit_id=1, location=(10, 20), timestamp=t(12, 30))
        store(unit_id=1, location=(11, 20), timestamp=t(12, 45))
        store(unit_id=1, location=(12, 20), timestamp=t(13, 00))
        store(unit_id=1, location=(10, 21), timestamp=t(12, 10))
        store(unit_id=1, location=(10, 22), timestamp=t(11, 30))
        store(unit_id=2, location=(10, 22), timestamp=t(11, 30))
        results = self.backend.query_last_position()
        self.assertEqual(results, {
            1: {
                'location': (12.0, 20.0),
                'timestamp': t(13, 00),
            },
            2: {
                'location': (10, 22),
                'timestamp': t(11, 30),
            },
        })

    def test_last_known_position_in_polygon(self):
        t = partial(datetime, 2012, 1, 1)
        store = lambda **kw: self.backend.store(**entry(**kw))
        store(unit_id=1, location=(50.07653, 14.43398), timestamp=t(12, 30))
        store(unit_id=1, location=(49.39668, 13.24951), timestamp=t(13, 00))
        store(unit_id=1, location=(49.00905, 17.18262), timestamp=t(12, 45))
        store(unit_id=2, location=(10, 21), timestamp=t(12, 10))
        store(unit_id=2, location=(10, 22), timestamp=t(11, 30))
        results = self.backend.query_last_position(in_polygon=(
            (51.65893, 14.76563),
            (47.79840, 10.70068),
            (48.45835, 21.48926),
            (51.65893, 14.76563),
        ))
        self.assertEqual(results, {
            1: {
                'location': (49.39668, 13.24951),
                'timestamp': datetime(2012, 1, 1, 13, 0),
            },
        })
