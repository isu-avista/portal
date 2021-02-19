from avista_portal.api import api_bp as bp
from flask import request, jsonify, current_app
from avista_data.device import Device
from avista_data.sensor import Sensor
from avista_data.data_point import DataPoint


def find_or_create_device(json):
    device = current_app.session.query(Device).filter_by(name=json.get("name")).first()
    if not device:
        device = Device(json)
        current_app.session.add(device)
        current_app.session.commit()
    return device


def find_or_create_sensor(json, device):
    sensor = current_app.session.query(Sensor).filter_by(name=json.get("name")).first()
    if not sensor:
        sensor = Sensor(json)
        current_app.session.add(sensor)
        current_app.session.commit()
    if sensor not in device.sensors:
        device.add_sensor(sensor)
        current_app.session.commit()

    return sensor


def create_point(json, sensor):
    point = DataPoint(json)
    current_app.session.add(point)
    current_app.session.commit()
    sensor.add_data_point(point)
    current_app.session.commit()


def process_data_async(json):
    with current_app.app_context():
        device = find_or_create_device(json['device'])
        data = json['data']
        for item in data:
            sensor = find_or_create_sensor(item['sensor'], device)
            points = item['data_points']
            for i in range(0, len(points)):
                create_point(points[i], sensor)


@bp.route('/api/data', methods=['POST'])
def add_data():
    if request.is_json:
        post_data = request.get_json()
        print(post_data)
        process_data_async(post_data)
        return jsonify({'status': 'success'})
    return jsonify({'status': 'failure'})
    # Now we need a processor which will process the data and add it to the database
    # preferably we will do this in a separate process, so we are not holding up the route
    # Thread(target=process_data_async, args=(post_data)).start()

