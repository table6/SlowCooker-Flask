# Prerequisites
## apt-get
- python3-pip
- mongodb-org (https://docs.mongodb.com/manual/tutorial/install-mongodb-on-ubuntu/)
## pip
- flask
- pymongo
- requests
- pytz

# Flask server
source $HOME/flask_server/bin/activate
export FLASK_APP=server.py
flask run --host=0.0.0.0

# MongoDB management
sudo service mongod [start/stop/restart]

