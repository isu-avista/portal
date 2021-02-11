from unittest.mock import MagicMock
from tests.api.base_api_test import BaseApiTest
from avista_data.server import Server
from avista_portal.data_transporter import DataTransporter
from avista_data import db
from avista_data.device import Device
from avista_data.sensor import Sensor
from avista_data.unit import Unit
from avista_data.data_point import DataPoint


class DataTransporterTest(BaseApiTest):

    def test_transfer(self):
        server = Server()
        server.set_name("Test Server")
        server.set_port(5005)
        server.set_ip_address("0.0.0.0")
        server.set_periodicity(5)
        db.session.add(server)
        db.session.commit()

        # need to mock the call to self.collect_data()
        dt = DataTransporter()
        dt.collect_data = MagicMock()
        dt.collect_data.return_value = dict(
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
                            name="DP2",
                            value=1.0,
                            timestamp=0,
                        ),
                        dict(
                            name="DP2",
                            value=2.0,
                            timestamp=1,
                        )
                    ],
                ),
            ]
        )
        dt.transfer()
        self.assertEqual(1, Device.query.count())
        dev = Device.query.get(1)
        print(f'Found Device: {dev}')
        self.assertEqual(1, dev.sensors.count())
        for s in dev.sensors:
            self.assertEqual(4, s.data.count())

    def test_collect_data(self):
        self.create_data()
        dt = DataTransporter()
        data = dt.collect_data()
        print(data)

    def test_clear_old_data(self):
        self.create_data()
        dt = DataTransporter()
        dt._markers.append(0)
        dt._markers.append(2)
        dt._markers.append(3)

        dt.clear_old_data()
        self.assertEqual(2, len(dt._markers))
        self.assertEqual(2, DataPoint.query.count())

    def create_data(self):
        dev = Device()
        dev.set_name("Test Device")
        dev.set_description("Description")
        dev.set_location("Place")
        db.session.add(dev)

        sens1 = Sensor()
        sens1.set_name("Sensor 1")
        sens1.set_unit(Unit.kWh)
        sens1.set_quantity("Power")
        sens1.set_class("Class1")
        sens1.set_module("Module1")
        db.session.add(sens1)
        dev.add_sensor(sens1)

        dp1 = DataPoint()
        dp1.set_name("DP1")
        dp1.set_value(1.0)
        dp1.set_timestamp(0)
        db.session.add(dp1)
        sens1.add_data_point(dp1)

        dp2 = DataPoint()
        dp2.set_name("DP1")
        dp2.set_value(2.0)
        dp2.set_timestamp(1)
        db.session.add(dp2)
        sens1.add_data_point(dp2)

        sens2 = Sensor()
        sens2.set_name("Sensor 2")
        sens2.set_unit(Unit.kWh)
        sens2.set_quantity("Power")
        sens2.set_class("Class2")
        sens2.set_module("Module2")
        db.session.add(sens2)
        dev.add_sensor(sens2)

        dp3 = DataPoint()
        dp3.set_name("DP2")
        dp3.set_value(1.0)
        dp3.set_timestamp(0)
        db.session.add(dp3)
        sens1.add_data_point(dp3)

        dp4 = DataPoint()
        dp4.set_name("DP2")
        dp4.set_value(2.0)
        dp4.set_timestamp(1)
        db.session.add(dp4)
        sens1.add_data_point(dp4)