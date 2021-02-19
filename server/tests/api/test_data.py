import unittest
from tests.api.base_api_test import BaseApiTest
from avista_data.device import Device
from flask import current_app


class DataTest(BaseApiTest):

    def test_data(self):
        data = dict(
            device=dict(
                name="Test",
                description="Test Device",
                location="Test Location",
            ),
            data=[
                dict(
                sensor=dict(
                    name="Sensor 1",
                    quantity="Test Quantity 1",
                    unit="kWh",
                    parameters=dict()
                ),
                data_points=[
                    dict(
                        name="DP1",
                        value=1.0,
                        timestamp=0,
                    ),
                    dict(
                        name="DP1",
                        value=2.0,
                        timestamp=1,
                    )
                ],
            ),
            ]
        )
        self.client.post('/api/data', json=data)
        self.assertEqual(1, current_app.session.query(Device).count())
        dev = current_app.session.query(Device).get(1)
        self.assertEqual(1, dev.sensors.count())
        for s in dev.sensors:
            self.assertEqual(2, s.data.count())


if __name__ == '__main__':
    unittest.main()
