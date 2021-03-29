import unittest
from tests.api.base_api_test import BaseApiTest
from avista_data.device import Device
from avista_data.issue import Issue
from avista_data.issue_type import IssueType
from flask import current_app


class DataTest(BaseApiTest):

    def get_data(self):
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
        return data

    def test_data(self):
        data = self.get_data()
        self.client.post('/api/data', json=data)
        self.assertEqual(1, current_app.session.query(Device).count())
        dev = current_app.session.query(Device).get(1)
        self.assertEqual(1, dev.sensors.count())
        for s in dev.sensors:
            self.assertEqual(2, s.data.count())

    def test_prediction_data(self):
        prediction_data = dict(
            predictions=[
                dict(
                value=0,
                type="NO_MAINT_REQD",
                name="name",
                description="no issue on device 123",
                device_id=124
                ),
                dict(
                value=1,
                type="MAINT_REQD",
                name="name",
                description="maintenance required on device 456",
                device_id=456
                )
            ]
        )
        self.client.post('/api/ml-data', json=prediction_data)
        self.assertEqual(1, current_app.session.query(Issue).count())
        issue = current_app.session.query(Issue).get(1)
        self.assertEqual(IssueType.MAINT_REQD, issue.type)


    def test_data_since(self):
        data = self.get_data()
        self.client.post('/api/data', json=data)
        response_1 = self.client.get('/api/data/0').json
        response_2 = self.client.get('/api/data/1').json
        self.assertEqual(2, len(response_1))
        self.assertEqual([1, 2.0, 1], response_2[0])




if __name__ == '__main__':
    unittest.main()
