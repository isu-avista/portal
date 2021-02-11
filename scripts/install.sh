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

# Collect the appropriate scripts and install them where they belong
# 1. need the docker compose script
# 2. need the startup script
# 3. need the run script

# Create the symbolic links

# Clean up installation files
