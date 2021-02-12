#!/bin/bash

# need to create a check to detect if docker is installed
# from https://raymii.org/s/snippets/Bash_Bits_Check_if_command_is_available.html

command_exists() {
	# check if command exists and fail otherwise
	command -v "$1" >/dev/null 2>&1
	if [[ $? -ne 0 ]]; then
		echo "$1 is required but it's not installed. Installing..."
		return 1
	fi
	return 0
}

# Install python3 if not already installed
command_exists "python3"
if [[ #? -ne 0 ]]; then
	sudo apt-get install python3 -y
fi

# Install docker if not already installed
command_exists "docker"
if [[ $? -ne 0 ]]; then
	curl -fsSL https://get.docker.com -o get-docker.sh
	sudo sh get-docker.sh
fi

# Install docker-compose if not already installed
command_exists "docker-compose"
if [[ $? -ne 0 ]]; then
	python3 -m pip install docker-compose
fi

# Install postgres if not already installed
command_exists "psql"
if [[ $? -ne 0 ]]; then
	sudo apt-get install postgresql libpq-dev postgresql-client postgresql-client-common -y
fi

# Generate and execute the database setup script
echo "CREATE DATABASE avistadb;" >> setup.sql
echo "CREATE USER avista WITH ENCRYPTED PASSWORD 'avistapw';" >> setup.sql
echo "GRANT ALL PRIVILEGES ON DATABASE avistadb TO avista;" >> setup.sql

sudo -u postgres psql -f setup.sql

# Create user
sudo adduser avista --system avista --no-create-home

# Create install directory
sudo mkdir /opt/avista

# Set directory permissions
sudo chmod 777 /opt/avista
sudo chown avista /opt/avista
sudo chgrp avista /opt/avista

cd /opt/avista

# Collect the appropriate scripts and install them where they belong
# 1. need the docker compose script
curl https://raw.githubusercontent.com/isu-avista/portal/master/docker-compose.yml

# 2. need the systemd service

curl https://raw.githubusercontent.com/isu-avista/portal/master/scripts/avista.service

# 3. Install, enable, and start the  systemd service

sudo mv avista.service /etc/systemd/system/avista.service

sudo systemctl enable avista
sudo systemctl start avista

