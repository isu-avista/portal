# get base image
FROM amd64/ubuntu

# Arguments
ARG dbtype
ARG dbname
ARG dbip
ARG dbport
ARG dbuser
ARG dbpass
ARG hostname
ARG hostport

# create working direcotry
WORKDIR ./

RUN apt-get update -y && apt-get upgrade -y
RUN apt-get install -y apt-utils
RUN apt-get install -y python3 python3-pip python-dev gunicorn3 python3-setuptools
RUN apt-get install -y git ssh libatlas-base-dev libpq-dev

# copy requirements
COPY ./requirements.txt ./requirements.txt

# install python dependencies
RUN pip3 install -r requirements.txt

# copy application files
COPY ./ ./

# Generate the config files
RUN python3 generate_configs.py -t $dbtype -n $dbname -i $dbip -o $dbport -p $dbpass -u $dbuser -s $hostname -r $hostport
