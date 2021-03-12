#!/bin/bash

# need to create a check to detect if docker is installed
# from https://raymii.org/s/snippets/Bash_Bits_Check_if_command_is_available.html

command_exists () {
	# check if command exists and fail otherwise
	command -v "$1" >/dev/null 2>&1
	if [[ $? -ne 0 ]]; then
		echo "$1 is required but it's not installed. Installing..."
		return 1
	fi
	return 0
}

# process input params
while getopts u:d:p: flag
do
    case "${flag}" in
        u) user=${OPTARG};;
        d) db=${OPTARG};;
        p) pass=${OPTARG};;
    esac
done

# Install python3 if not already installed
command_exists "python3"
if [[ $? -ne 0 ]]; then
  apt-get install python3 -y
fi

# Install pip if not already installed
command_exists "python3 -m pip"
if [[ $? -ne 0 ]]; then
  apt-get install python3-pip -y
fi

command_exists "curl"
if [[ $? -ne 0 ]]; then
  apt-get install curl -y
fi

# Install docker if not already installed
command_exists "docker"
if [[ $? -ne 0 ]]; then
  curl -fsSL https://get.docker.com -o get-docker.sh
  sh get-docker.sh
fi

# Install docker-compose if not already installed
command_exists "docker-compose"
if [[ $? -ne 0 ]]; then
  python3 -m pip install docker-compose
fi

# Install postgres if not already installed
command_exists "psql"
if [[ $? -ne 0 ]]; then
  apt-get install postgresql libpq-dev postgresql-client postgresql-client-common -y
fi

# Generate and execute the database setup script
echo "CREATE DATABASE $db;" > setup.sql
echo "CREATE USER $user WITH ENCRYPTED PASSWORD '$pass';" >> setup.sql
echo "GRANT ALL PRIVILEGES ON DATABASE $db TO $user;" >> setup.sql

sudo -u postgres psql -f setup.sql

# Create user
adduser --no-create-home --system avista
groupadd avista
groupadd docker
usermod -aG docker avista
usermod -aG avista avista
systemctl restart docker

# Create install directory
mkdir /opt/avista

# Set directory permissions
chmod 777 /opt/avista
chown avista /opt/avista
chgrp avista /opt/avista

cd /opt/avista

# Collect the appropriate scripts and install them where they belong
# 1. need the docker compose script
curl https://raw.githubusercontent.com/isu-avista/portal/master/docker-compose.yml -o docker-compose.yml
mv docker-compose.yml /opt/avista/avista.yml

# 2. need the systemd service

curl https://raw.githubusercontent.com/isu-avista/portal/master/scripts/avista.service -o avista.service

# 3. Install, enable, and start the  systemd service

mv avista.service /etc/systemd/system/avista.service

systemctl enable avista
systemctl start avista
