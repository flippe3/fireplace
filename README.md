# [General Documentation](https://github.com/flippe3/fireplace/blob/main/DesignDecisions.md)

## Napkin Sketch
## ![Napkin sketch](https://github.com/flippe3/fireplace/blob/main/references/napkin_sketch.jpg?raw=true)

# [API Documentation](https://github.com/flippe3/fireplace/blob/main/APIDocumentation.md)

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
You will also have to change the IP addresses to match your IP addresses and make sure the paths are correct to your server in `app.py`, `API/api.py`, `simulator.py`.

### Simulator API key
The simulator also needs an API key from [weather api](https://www.weatherapi.com/) so you will need an account and generate an api key and store that in `~/.weather_key`.

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

# Functionality of the website
With the website, it is possible to find fireplaces in and around Luleå. When routing to it, the user can see the map with fireplaces, click on a marker and on the link to access a detail page. Additionally, a user can log in and after logging in, it can also receive an API token by clicking on the username in the right top corner or logout. Another functionality is to create fireplaces by clicking on the create button and to book a slot when to go to a fireplace, to change the value of the simulator for a certain point in time. If the logged-in user is an admin, it is also possible to see an overview of all the users and to delete them. This site is opened by pressing the button Users.