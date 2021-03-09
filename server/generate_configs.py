import uuid
import yaml
import argparse
import os


def init_argparse() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        usage="%(prog)s [OPTIONS] ...",
        description="Generate configuration files for Avista IoT",
        epilog="Copyright (C) 2020, 2021 Idaho State University Empirical SE Lab"
    )
    parser.add_argument("-t", "--dbtype", action="store", type=str, required=True, help="DBMS Type")
    parser.add_argument("-n", "--dbname", action="store", type=str, required=True, help="DBMS Name")
    parser.add_argument("-i", "--dbip", action="store", type=str, required=True, help="DBMS IP/Hostname")
    parser.add_argument("-o", "--dbport", action="store", type=str, required=True, help="DBMS Port")
    parser.add_argument("-p", "--dbpass", action="store", type=str, required=True, help="DBMS Password")
    parser.add_argument("-u", "--dbuser", action="store", type=str, required=True, help="DBMS Username")
    parser.add_argument("-s", "--hostname", action="store", type=str, required=True, help="Server Host Name")
    parser.add_argument("-r", "--hostport", action="store", type=str, required=True, help="Server Host Port")
    parser.add_argument("-v", "--version", action="version", version=f'{parser.prog} version 1.0.0')

    return parser

def generate_logs_directory():
    if not os.path.is_dir('logs'):
        os.mkdir('logs')
        open('logs/server.log', 'w').close()


def generate_flask_config():
    config = {
        'ENV': 'production',
        'TESTING': False,
        'DEBUG': False,
        'JWT_SECRET_KEY': uuid.uuid4().hex,
        'SECRET_KEY': uuid.uuid4().hex,
        'SQLALCHEMY_TRACK_MODIFICATIONS': False
    }
    with open('conf/flask.yml', 'w') as outfile:
        yaml.dump(config, outfile, default_flow_style=False)


def generate_server_config(dbtype, dbname, dbip, dbport, dbuser, dbpass, hostname, hostport):
    config = {
        "sysdata": [
            {
                "item": "System Identifier",
                "value": uuid.uuid4().hex,
                "type": "text",
            },
            {
                "item": "Equipment Monitored",
                "value": "",
                "type": "text",
            },
            {
                'item': 'Location',
                'value': '',
                'type': 'text',
            },
            {
                'item': 'Data Collection Periodicity (ms)',
                'value': 5000,
                'type': 'number',
            },
            {
                'item': 'Server Port',
                'value': 5000,
                'type': 'number',
            }
        ],
        'dbdata': [
            {
                'item': 'DBMS Type',
                'value': dbtype,
                'type': 'text',
            },
            {
                'item': 'DBMS DB Name',
                'value': dbname,
                'type': 'text',
            },
            {
                'item': 'DBMS IP Address',
                'value': dbip,
                'type': 'text',
            },
            {
                'item': 'DBMS Port',
                'value': dbport,
                'type': 'text',
            },
            {
                'item': 'DBMS Username',
                'value': dbuser,
                'type': 'text',
            },
            {
                'item': 'DBMS Password',
                'value': dbpass,
                'type': 'password',
            }
        ],
        'service': {
            'host': hostname,
            'port': hostport,
        }
    }

    with open('conf/config.yml', 'w') as outfile:
        yaml.dump(config, outfile, default_flow_style=False)


def main() -> None:
    parser = init_argparse()
    args = parser.parse_args()
    dic = vars(args)

    dbtype = dic['dbtype']
    dbname = dic['dbname']
    dbip = dic['dbip']
    dbport = dic['dbport']
    dbpass = dic['dbpass']
    dbuser = dic['dbuser']
    host = dic['hostname']
    port = dic['hostport']

    generate_server_config(dbtype, dbname, dbip, dbport, dbuser, dbpass, host, port)
    generate_flask_config()
    generate_logs_directory()


if __name__ == '__main__':
    main()
