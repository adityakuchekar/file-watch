# File-Watch
File-Watch is a realtime dierctory monitoring application. Given a directory path on your local system, the application tracks changes done to this directory in real time and outputs the change log also.

## Technologies Used

- Python Flask ->  for basic http server
- Python Watchdog -> to monitor a directory in real time
- Angular -> for frontend application
- Docker -> used for packaging the app and deploying it

## Functioning

In order to track real time changes made to a local directory, I have used python's watchdog module which internally uses linux inotify tool. Watchdog emits events of the directory changes and they are stored in a in-memory queue. The flask app uses Server Sent Events(SSE) to stream these changes by polling the queue and send an event as response to the frontend application.

## Note
The application is tested on linux based Ubuntu system(Ubuntu 20.04 LTS). It has not been tested as such for a windows/mac system.

## Prerequisite
Docker is required in order to deploy this application locally

### Installing Docker (If not present)
```bash
 # Older versions of Docker were called docker, docker.io, or docker-engine. If these are installed, uninstall them:
 sudo apt-get remove docker docker-engine docker.io containerd runc

 # Update the apt package index, and install the latest version of Docker
 sudo apt-get update
 sudo apt-get install docker-ce docker-ce-cli containerd.io docker-compose-plugin
```


## Deploying the application locally

### BACKEND


```bash
docker run -d -p 5000:5000 --name flask-api -v <directory_path_to_monitor>:/datavol aditya13101996/pywatch

# replace <directory_path_to_monitor> with the path you want to monitor
# for eg: docker run -d -p 5000:5000 --name flask-api -v /home/user/watchfolder:/datavol aditya13101996/pywatch
# changes in /home/user/watchfolder will be monitored
```
- A development flask server is spawned locally using the docker image **aditya13101996/pywatch**
- It runs on port 5000


### FRONTEND


```bash
docker run -d -p 4200:4200 --name frontend-app aditya13101996/filewatch
```
- A development angular server is spawned locally using the docker image **aditya13101996/filewatch**
- It runs on port 4200


## RUN and TEST the application
- Open any browser and type **localhost:4200**
- The application will start. Click on Watch button on the app to start monitoring the changes
- If you want to stop monitoring, click on Stop & Clear Button on the app