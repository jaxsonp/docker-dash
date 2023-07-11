# Docker Dash
Docker Dash is a handy GUI dashboard made for administrators to manage apps running as docker containers on a server.

## Table of Contents
1. [Background](#background)
1. [Getting Started](#getting-started)
1. [Docker Dash API](#docker-dash-api)

<br>

---

<br>

# Background

This project was created as a mockup to demonstrate the concept of containerization of applications and to prototype an administrative dashboard to manage users and apps. With that in mind, safety and security were not the highest concern. Be advised that significant security vulnerabilities may exist in many aspects of this project.

<br>

# Getting Started

*TODO put stuff here*

<br>

# Docker Dash API

Detailed documentation of the Docker Dash API and its methods can be found at `server/README.md` or at [this link](https://github.com/JaxsonP/docker-dash/tree/master/server#readme).

## Overview

This API serves as a backend for Docker Dash, providing an interface between the docker and the dashboard. Functionality includes creating, running, and killing apps, as well as getting an app's status, resource usage, and uptime logs. This API also includes support for Docker's swarm mode, however due to the nature of swarm mode, it's functionality varies significantly from Docker without swarm mode, which will be referred to as solo mode. All files relevant to the API are located in the `server/` folder.

## Setup Guide

### Prerequisites:
- CentOS 7
- Internet connection
- All nodes must have unique hostnames *(for swarm mode)*

*Notes: Installation should ideally work on other Red-Hat-based distros, but it hasn't been formally tested.*

### For Solo Mode:

Run this command (you may be asked for sudo password):
``` bash
bash <(curl -s https://raw.githubusercontent.com/JaxsonP/docker-dash/master/server/scripts/solo_install.sh)
```
This will download all files and install and configure Docker and Python 3.9.16. This can take up to 5-10 minutes. You will be prompted to restart, then run the `start-server` script to start the API. If you are in the `docker-dash` folder the command will be:
``` bash
./start-server
```

### For Swarm Mode:

Run this command (you may be asked for sudo password):
``` bash
bash <(curl -s https://raw.githubusercontent.com/JaxsonP/docker-dash/master/server/scripts/swarm_install.sh)
```
This will download all files and install and configure Docker and Python 3.9.16. This can take up to 5-10 minutes. You will be prompted to restart, and you can start setting up the worker nodes. The specific command to use will be saved in a file called `join_command.txt`, but it should look something like:
``` bash
bash <(curl -s https://raw.githubusercontent.com/JaxsonP/docker-dash/master/server/scripts/swarm_install_worker.sh) [SWARM_TOKEN] [MANAGER_IP_ADDRESS]:2377
```
Run this command on each worker node to complete setup. This script will first add the node to the swarm as a manager so that it can configure itself, then it will demote itself to worker. Once that is done, you can navigate to the `docker-dash/` directory on the true manager node and start the server with:
``` bash
./start-server
```