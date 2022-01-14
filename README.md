# General Documentation

## Napkin Sketch
## ![Napkin sketch](https://github.com/flippe3/fireplace/blob/main/references/napkin_sketch.jpg?raw=true)

# [API Documentation](https://github.com/flippe3/fireplace/blob/main/references/api_sketch.jpg)

# [Time Log](https://github.com/flippe3/fireplace/blob/main/references/Timelog.xlsx)

# Deployment protocol

## Prerequisite
* Ubuntu 18.04 server with around 4gb ram and 10gb memory.
* Python 3.8.10
* Install [Jenkins](https://www.jenkins.io/doc/book/installing/linux/) 

## Installation
### Download the repository
```
git clone https://github.com/flippe3/fireplace.git
cd fireplace
```
### Install the requirements
```
pip3 install -r requirements.txt
```
### Setup the database
Use [this](https://github.com/flippe3/fireplace/blob/main/MysqlDatabaseSetup.sql) database setup.

### Changing database passwords
In `app.py` and `API/api.py`, you will have to enter the database username and password and also the IP for the database.

### Changing IP addresses
You will also have to change the IP addresses to match your IP addresses.

### Setup services
Now we have everything necessary to setup the website and to do so we have to start the systemd services that are included in the github repository. You may have to change paths in the .service files. To setup the files simply start the systemd services.
```
systemctl enable api.service
systemctl enable lowlevel_api.service
systemctl enable app.service
systemctl enable simulator.service
systemctl start api.service
systemctl start lowlevel_api.service
systemctl start app.service
systemctl start simulator.service
```


