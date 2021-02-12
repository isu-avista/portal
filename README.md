# Avista-Portal

## Description

This is the Portal module providing the data aggregation

## Table of Contents

1. [Installation](#installation)
2. [Usage](#usage)
3. [Credits](#credits)
4. [License](#license)

## Installation

To install this use the following command.

```
curl https://raw.githubusercontent.com/isu-avista/portal/master/scripts/install.sh
sudo bash ./install.sh
```

## Usage

### Database Setup

```bash
flask db init
flask db upgrade
```

### Executing the Production Environment

In the project root directory execute the following command

```
docker-compose up -f docker-compose.yml
```

### Executing the Development Environment

#### Server

From the project root directory:

```bash
source env/bin/activate
cd server
python3 app.py
```

#### Client

From the project root directory:

```bash
cd client
npm run serve
```

### Server Configuration

There are three configuration files:
* .flaskenv - this contains the necessary environment variables needed.
  - CONFIG_PATH - the absolute or relative path to the configuration files. Typically: "./conf"
  - LOG_PATH - the absolute or relative path to the logging directory. Typically: "./logs"
* Config files in the "conf" directory:
  - `flask.yml` - This contains the flask configuration information and should look something like:
  ```yaml
    ---
    ENV: 'development'
    SERVER_NAME: 'localhost:5000'
    TESTING: True
    DEBUG: True
    JWT_SECRET_KEY: TEST_KEY
    SECRET_KEY: TEST_KEY
    SQLALCHEMY_DATABASE_URI: 'sqlite:///./app.db'
    SQLALCHEMY_TRACK_MODIFICATIONS: False
  ```
  Note that the `JWT_SECRET_KEY` and `SECRET_KEY` should be generated and not stored anywhere
  unauthorized individuals may access it.
  - `config.yml` - This contains information needed to configure the server, and looks something
  like the following:
  ```yaml
    ---
    sysdata:
      -
        item: System Identifier
        value: uuid.uuid4().hex
        type: text
      -
        item: Equipment Monitored
        value: Dryer 01
        type: text
      -
        item: Location
        value: ERC Rm 202
        type: text
      -
        item: Data Collection Periodicity (ms)
        value: 5000
        type: number
      -
        item: Server Port
        value: 5000
        type: number
    dbdata:
      -
        item: DBMS IP Address
        value: '127.0.0.1'
        type: text
      -
        item: DBMS Port
        value: 3306
        type: number
      -
        item: DBMS Username
        value: service
        type: text
      -
        item: DBMS Password
        value: '*******'
        type: password
  ```
  
#### Generating Secret Keys

```bash
python3 -c "import uuid; print(uuid.uuid4().hex)"
```

## Credits

This module was contributed by:

- Isaac D. Griffith

## License

Copyright (c) 2020, 2021 Idaho State University Empirical Software Engineering Laboratory

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

