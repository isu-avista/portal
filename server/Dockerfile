FROM amd64/ubuntu

WORKDIR ./

RUN apt-get update -y
RUN apt-get install -y python3 python3-pip python-dev gunicorn3 python3-setuptools
RUN apt-get install -y git ssh
RUN apt-get install -y libatlas-base-dev
RUN apt-get install -y libpq-dev

COPY ./requirements.txt ./requirements.txt

RUN pip3 install -r requirements.txt

COPY ./ ./
