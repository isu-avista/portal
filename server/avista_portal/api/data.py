from avista_portal.api import api_bp as bp
from flask import request, jsonify
from threading import Thread
from avista_data import db
from avista_data import current_app as app
from avista_data.device import Device
from avista_data.sensor import Sensor
from avista_data.data_point import DataPoint


def find_or_create_device(json):
    device = Device.query.filter_by(name=json.get("name")).first()
    print(f'device: {device}')
    if not device:
        device = Device(json)
        db.session.add(device)
        db.session.commit()
    return device


def find_or_create_sensor(json, device):
    sensor = Sensor.query.filter_by(name=json.get("name")).first()
    print()
    print(f'sensor: {json}')
    print(f'found: {sensor}')
    if not sensor:
        sensor = Sensor(json)
        db.session.add(sensor)
        db.session.commit()
    if sensor not in device.sensors:
        device.add_sensor(sensor)

    print(f'Found Sensor: {sensor}')
    return sensor


def create_point(json, sensor):
    point = DataPoint(json)
    db.session.add(point)
    db.session.commit()
    sensor.add_data_point(point)


def process_data_async(json):
    with app.app_context():
        device = find_or_create_device(json['device'])
        data = json['data']
        print(f'data: {data}')
        for item in data:
            sensor = find_or_create_sensor(item['sensor'], device)
            points = item['data_points']
            for i in range(0, len(points)):
                create_point(points[i], sensor)


@bp.route('/api/data', methods=['POST'])
def add_data():
    response_object = {'status': 'success'}
    print(f'Is Json? {request.is_json}')
    if request.is_json:
        post_data = request.get_json()
        print(post_data)
        process_data_async(post_data)
    return jsonify(response_object)
    # Now we need a processor which will process the data and add it to the database
    # preferably we will do this in a separate process, so we are not holding up the route
    # Thread(target=process_data_async, args=(post_data)).start()

