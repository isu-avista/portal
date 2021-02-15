# Avista-Portal

## Description

This is the Portal module providing the data aggregation

## Table of Contents

1. [Installation](#installation)
2. [Usage](#usage)
3. [Credits](#credits)
4. [License](#license)

## Installation

1. Retrieve the install script:

   ```shell
   curl -fsSL https://raw.githubusercontent.com/isu-avista/portal/master/scripts/install.sh -o install.sh
   ```
 
2. Make the script executable

   ```shell
   chmod +x install.sh
   ```
   
3. Execute the install script as sudo

   ```shell
   sudo ./install.sh -u avista -d avistadb -p avistapw
   ```
   
   The options are based on the default setup that comes with the image
   - u : sets the username to be used in the database
   - p : sets the password for the database
   - d : sets the database name

This process will create the folder `/opt/avista` where the docker-compose file will reside.
It will setup a service based on this file that will be used to start the system on startup.
Finally, it will setup the database using the command line arguments.
   
## Building and executing with Docker

1. Build docker images (this part still requires an ssh key authorized with github)

   1. Login to docker to be able to push the docker images to dockerhub
   
      ```shell
      docker login --username <your-username> --password <your-password>
      ```
   
   2. Build the server image, from the project root directory

      ```shell
      cd server
      docker build \
             --build-arg dbtype=postgres \
             --build-arg dbname=avistadb \
             --build-arg dbuser=avista \
             --build-arg dbpass=avistapw \
             --build-arg dbip=localhost \
             --build-arg dbport=5432 \
             --build-arg hostname=localhost \
             --build-arg port=5000 \
             -t isuese/avista-portal-server:latest .
      docker push isuese/avista-portal-server:latest
      ```
      
   3. Build the client image, from the project root directory:
   
      ```shell
      cd client
      docker build -t isuese/avista-portal-client:latest .
      docker push isuese/avista-portal-client:latest
      ```

2. If the build was error free, the images can now be spun up in containers. From the project root directory
   ```shell
   sudo docker-compose up
   ```

## Usage

### Database Setup

```bash
flask db init
flask db upgrade
```

### Executing the Production Environment

In the project root directory execute the following command

```shell
docker-compose up -f docker-compose.yml
```

### Executing the Development Environment

#### Server

From the project root directory:

```shell
source env/bin/activate
cd server
python3 app.py
```

#### Client

From the project root directory:

```shell
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

```shell
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

