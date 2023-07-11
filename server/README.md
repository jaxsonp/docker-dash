# Docker Dash API

This API can be used to manage apps running as Docker containers on a server. Functionality includes creating, running, and killing apps, as well as getting an app's status, resource usage, and uptime logs. This API also supports Docker in swarm mode, which runs on a cluster of servers that shares tasks with automatic load balancing. This API was created for demo purposes, so it is not intended to run on systems where security is paramount.

This is a comprehensive guide of the entire API but a quick plaintext outline of all endpoints can be found at the base url.

## Table of Contents:

1. [General Notes](#general-notes)
1. [Setup Guide](#setup-guide)
1. [API Endpoints (usage and examples)](#api-endpoints)

</br>
</br>

# General notes

### Naming Conventions

When an app is created, the image and user name are provided, then the Docker container is made with the name `"[IMAGE_NAME]--[USER_NAME]"`. All subsequent references to this container will use this name.

Usernames and image names can include uppercase and lowercase letters and numbers, as well as dashes, underscores. However, usernames cannot have double dashes, nor can they start with a dash because a double dash is used to deliminate the username from the image name in the container naming convention. Image names in docker hub are already unique, but user names must be unique as well.

### Server ID

Each server will be identified by a unique key in order to specify which one to interface with. For demo purposes, this API only responds to a placeholder server with the ID "demo", however in production this is how you would specify your seperate servers.

### Solo Mode vs Swarm Mode

This API has methods for working with a standard docker setup as well as as docker's swarm mode. Swarm mode is a way to load balance apps across a cluster of servers, where one manager node delegates tasks amongst itself and its worker nodes. You can read more about Docker swarm mode [here](#https://docs.docker.com/engine/swarm/key-concepts/). Solo mode is the term used for docker's standard functionality, with just one node hosting containers. Because swarm mode uses services instead of standard containers, there are many key differences between these two modes:

| | Solo mode | Swarm mode |
|:-|:-|:-|
| Starting/stopping/restarting | Yes | No |
| Pausing/unpausing | Yes | No |
| Created apps are started | Manually | Upon creation |
| Persistent state after completion | Yes | No |

*Note: The word "container" is generally associated with solo mode, and the word "service" is generally associated with swarm mode, however both are interchangeable with the word "app"*

### Get Request Output

Most GET methods this API provides return data from a corresponding docker command. If you want more information about a method or what it returns, check out the [docker documentation](https://docs.docker.com/engine/reference/commandline/cli/) about that command for a more direct explanation.

</br>
</br>

# Setup Guide:

## Prerequisites:

- CentOS 7
- Internet connection
- All nodes must have unique hostnames (swarm mode)

## For Solo Mode:

Run this command (you may be asked for sudo password):
``` bash
bash <(curl -s https://raw.githubusercontent.com/JaxsonP/docker-dash/master/server/scripts/solo_install.sh)
```
This will download all files and install and configure Docker and Python 3.9.16. This can take up to 5-10 minutes. You will be prompted to restart, then run the `start-server` script to start the API. If you are in the `docker-dash/` folder the command will be:
``` bash
./start-server
```

## For Swarm Mode:

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
*Note: In order to run main.py, you must either explicitly use venv/bin/python (like shown) or manually activate the virtual environment with `source venv/bin/activate`.*

</br>
</br>

# API Endpoints:

1. [Start App](#start-app)
1. [Stop App](#stop-app)
1. [Pause App](#pause-app)
1. [Unpause App](#unpause-app)
1. [Restart App](#restart-app)
1. [Kill App](#kill-app)
1. [Create App](#create-app)
1. [Delete App](#delete-app)
1. [Hard Reset App](#hard-reset-app)
1. [Get Users](#get-users)
1. [Get App Names](#get-app-names)
1. [Get App Status](#get-app-status)
1. [Get App Stats](#get-app-stats)
1. [Get App Info](#get-app-info)
1. [Get Node Names](#get-node-names)
1. [Get Node Status](#get-node-status)
1. [Get Node Info](#get-node-info)
1. [Get App Uptime Summary](#get-app-uptime-summary)
1. [Request Image](#request-image)
1. [Get Images](#get-images)



</br>

## Start App

### Usage:

``` 
<POST> http://placeholder.url/[SERVER_ID]/start-app?name=[APP_NAME]
```

### Mode:

This method is compatible with solo mode only.

### Description:

Starts the specified app using the `docker start` command. Trying to start an app that is paused will return an error, a paused app must be unpaused.

`SERVER_ID` - Server-specific identifier

`APP_NAME` - Name of app to start, following the [naming conventions](#naming-conventions).

</br>

## Stop App

### Usage:

```
<POST> http://placeholder.url/[SERVER_ID]/stop-app?name=[APP_NAME]
```

### Mode:

This method is compatible with solo mode only.

### Description:

Signals for the specified app to exit using the `docker stop` command. If the container does not respond to the `SIGTERM` signal within a 10 second grace period, it will kill the container forcefully with `SIGKILL`.

`SERVER_ID` - Server-specific identifier

`APP_NAME` - Name of app to stop, following the [naming conventions](#naming-conventions).

</br>

## Pause App

### Usage:

```
<POST> http://placeholder.url/[SERVER_ID]/pause-app?name=[APP_NAME]
```

### Mode:

This method is compatible with solo mode only.

### Description:

Pauses the specified app using the `docker pause` command. An app must be already running in order to be paused, otherwise the api will return error. While an app is paused, it can be unpaused, stopped, restarted, or killed.

`SERVER_ID` - Server-specific identifier

`APP_NAME` - Name of app to pause, following the [naming conventions](#naming-conventions).

</br>

## Unpause App

### Usage:

```
<POST> http://placeholder.url/[SERVER_ID]/unpause-app?name=[APP_NAME]
```

### Mode:

This method is compatible with solo mode only.

### Description:

Unpauses the specified app using the `docker unpause` command. An app must be paused, otherwise the api will return error.

`SERVER_ID` - Server-specific identifier

`APP_NAME` - Name of app to unpause, following the [naming conventions](#naming-conventions).

</br>

## Restart App

### Usage:

```
<POST> http://placeholder.url/[SERVER_ID]/restart-app?name=[APP_NAME]
```

### Mode:

This method is compatible with solo mode only.

### Description:

Restarts the specified app using the `docker restart` command. This command behaves similarly to a `docker stop` then a `docker start` command.

`SERVER_ID` - Server-specific identifier

`APP_NAME` - Name of app to restart, following the [naming conventions](#naming-conventions).

</br>

## Kill App

### Usage:

```
<POST> http://placeholder.url/[SERVER_ID]/kill-app?name=[APP_NAME]
```

### Mode:

This method is compatible with both solo and swarm mode.

### Description:

Kills the specified app by forcefully stopping the container with a `SIGKILL` signal. Not as graceful as the [Stop App](#stop-app) method, and therefore not recommended.

`SERVER_ID` - Server-specific identifier

`APP_NAME` - Name of app to kill, following the [naming conventions](#naming-conventions).

</br>

## Create App

### Usage:

```
<POST> http://placeholder.url/[SERVER_ID]/create-app?image=[IMAGE_NAME]&user=[USER_NAME]
```

### Mode:

This method is compatible with both solo and swarm mode.

### Description:

Creates an app instance using the image specified. Once created, the container will be called '`IMAGE_NAME`--`USER_NAME`'. The image must have already been requested and approved in order to be used to create an app.

`SERVER_ID` - Server-specific identifier

`IMAGE_NAME` - Name of the image to load the app from

`USER_NAME` - Name of the user who is using the app

</br>

## Delete App

### Usage:

```
<POST> http://placeholder.url/[SERVER_ID]/delete-app?name=[APP_NAME]
```

### Mode:

This method is compatible with solo mode only.

### Description:

Deletes the specified app, removing ALL related data.

`SERVER_ID` - Server-specific identifier

`APP_NAME` - Name of app to delete, following the [naming conventions](#naming-conventions).

</br>

## Hard Reset App

### Usage:

```
<POST> http://placeholder.url/[SERVER_ID]/hard-reset-app?name=[APP_NAME]
```

### Mode:

This method is compatible with solo mode only.

### Description:

Resets the specified app, clearing ALL data and restoring it from the original image. Under the hood this method stops and deletes the app instance, then recreates it from the source image.

`SERVER_ID` - Server-specific identifier

`APP_NAME` - Name of app to reset, following the [naming conventions](#naming-conventions).

</br>

## Get Users

### Usage:

```
<GET> http://placeholder.url/[SERVER_ID]/get-users
```

### Mode:

This method is compatible with both solo and swarm mode.

### Description:

Returns an array of all users that have apps (either running or stopped) on the specified server

`SERVER_ID` - Server-specific identifier

### Example Response:
``` json
["john", "admin", "sarah"]
```

</br>

## Get App Names

### Usage:

```
<GET> http://placeholder.url/[SERVER_ID]/get-app-names?user=[USER]
```

### Mode:

This method is compatible with both solo and swarm mode.

### Description:

Returns an array of all existing apps on the specified server, regardless of its state (e.g. running, exited). If the `USER` parameter is not omitted, only the apps belonging to the given user will be returned

`SERVER_ID` - Server-specific identifier

`USER` _(optional)_ : Name of user to query for

### Example Response:
``` json
["jupyter-lab--john", "xterm--admin", "httpd--sarah"]
```

</br>

## Get App Status

### Usage:

```
<GET> http://placeholder.url/[SERVER_ID]/get-app-status?name=[APP_NAME]
```

### Mode:

This method is compatible with both solo and swarm mode.

### Description:

Returns basic information and status, in json format. This method returns the output of the `docker ps` commmand. Returns app resource information in json format, using the `docker stats` commmand. In swarm mode, it uses ssh to get info from the required node, so it may break if there are problems with the network or ssh configuration.

`SERVER_ID` - Server-specific identifier

`APP_NAME` _(optional)_ : Name of app to query, following the [naming conventions](#naming-conventions). If omitted, will return a list of all apps and statuses.

### Example Response:
``` json
{
  "Command": "\"/docker-entrypoint.…\"",
  "CreatedAt": "2021-03-10 00:15:05 +0100 CET",
  "ID": "a762a2b37a1d",
  "Image": "jupyter-lab",
  "Labels": "",
  "LocalVolumes": "0",
  "Mounts": "",
  "Names": "jupyter-lab",
  "Networks": "bridge",
  "Ports": "80/tcp",
  "RunningFor": "4 seconds ago",
  "Size": "0B",
  "State": "running",
  "Status": "Up 3 seconds"
}
```

</br>

## Get App Stats

### Usage:

```
<GET> http://placeholder.url/[SERVER_ID]/get-app-stats?name=[APP_NAME]
```

### Mode:

This method is compatible with both solo and swarm mode.

### Description:

Returns app resource information in json format, using the `docker stats` commmand. In swarm mode, this method uses ssh to get info from the required node, so it may break if there are problems with the network or ssh configuration.

`SERVER_ID` - Server-specific identifier

`APP_NAME` _(optional)_ : Name of app to query, following the [naming conventions](#naming-conventions). If omitted, will return a list of all apps' information.

### Example Response:
``` json
{
  "BlockIO": "0B / 0B",
  "CPUPerc": "0.02%",
  "Container": "0203b8e9c65b",
  "ID": "0203b8e9c65b",
  "MemPerc": "0.38%",
  "MemUsage": "29.92MiB / 7.668GiB",
  "Name": "testcontainer",
  "NetIO": "1.01kB / 0B",
  "PIDs": "82"
}
```

</br>

## Get App Info

### Usage:

```
<GET> http://placeholder.url/[SERVER_ID]/get-app-info?name=[APP_NAME]
```

### Mode:

This method is compatible with both solo and swarm mode.

### Description:

Returns detailed information of specified app, in json format. This method uses the `docker inspect` commmand, it will return identical data.

`SERVER_ID` - Server-specific identifier

`APP_NAME` - Name of app to query, following the [naming conventions](#naming-conventions).

### Example Response:
``` json
{
  "Id": "d2cc496561d6d520cbc0236b4ba88c362c446a7619992123f11c809cded25b47",
  "Created": "2015-06-08T16:18:02.505155285Z",
  "Path": "bash",
  "Args": [],
  "State": {
    "Running": false,
    "Paused": false,
    "Restarting": false,
    "OOMKilled": false,
    "Dead": false,
    "Pid": 0,
    "ExitCode": 0,
    "Error": "",
    "StartedAt": "2015-06-08T16:18:03.643865954Z",
    "FinishedAt": "2015-06-08T16:57:06.448552862Z"
  },
  "Image": "ded7cd95e059788f2586a51c275a4f151653779d6a7f4dad77c2bd34601d94e4",
  "NetworkSettings": {
    "Bridge": "",
    "SandboxID": "6b4851d1903e16dd6a567bd526553a86664361f31036eaaa2f8454d6f4611f6f",
    "HairpinMode": false,
    "LinkLocalIPv6Address": "",
    "LinkLocalIPv6PrefixLen": 0,
    "Ports": {},
    "SandboxKey": "/var/run/docker/netns/6b4851d1903e",
    "SecondaryIPAddresses": null,
    "SecondaryIPv6Addresses": null,
... continues for >100 lines ...
```

</br>

## Get Node Names

### Usage:

```
<GET> http://placeholder.url/[SERVER_ID]/get-node-names
```

### Mode:

This method is compatible with both solo and swarm mode.

### Description:

Returns an array of the hostnames of all nodes in the swarm, or if the node is running in solo mode, it will return a list who's only element is its own hostname.

`SERVER_ID` - Server-specific identifier

### Example Response:
``` json
["localhost.server1", "localhost.server2", "localhost.server3"]
```

</br>

## Get Node Status

### Usage:

```
<GET> http://placeholder.url/[SERVER_ID]/get-node-status?hostname=[HOSTNAME]
```

### Mode:

This method is compatible with both solo and swarm mode.

### Description:

Returns basic status info about nodes in a swarm network, in json format. Under the hood, this method returns the output of `docker node ls`. If the node is not in swarm mode, it will still return it's own status info in an array with length 1, albiet some fields are unobtainable in solo mode and will be omitted.

`SERVER_ID` - Server-specific identifier

`HOSTNAME` _(optional)_ - Hostname of the node to query. If omitted, will return a list of all nodes and their statuses.

### Example Response:
``` json
{
   "Availability":"Active",
   "Hostname":"localhost.server2",
   "ManagerStatus":"Leader",
   "Self":false,
   "Status":"Ready",
}
```

</br>

## Get Node Info

### Usage:

```
<GET> http://placeholder.url/[SERVER_ID]/get-node-info?hostname=[HOSTNAME]
```

### Mode:

This method is compatible with swarm mode only.

### Description:

Returns detailed information of a specific node in the swarm network, in json format. Under the hood, this method uses the `docker node inspect` commmand, it will return identical data.

`SERVER_ID` - Server-specific identifier

`HOSTNAME` - Hostname of the node to query

### Example Response:
``` json
[
  {
    "ID": "dnv2tbnt2kcpgw90o3dvo99x2",
    "Version": {
      "Index": 361
    },
    "CreatedAt": "2023-06-27T20:26:14.950110744Z",
    "UpdatedAt": "2023-06-30T18:38:13.305299037Z",
    "Spec": {
      "Labels": {
        
      },
      "Role": "worker",
      "Availability": "active"
    },
    "Description": {
      "Hostname": "localhost.server2",
      "Platform": {
        "Architecture": "x86_64",
        "OS": "linux"
      },
      "Resources": {
        "NanoCPUs": 1000000000,
        "MemoryBytes": 1927254016
      },
      "Engine": {
        "EngineVersion": "24.0.2",
        "Plugins": [
          {
            "Type": "Log",
            "Name": "awslogs"
          },
          {
            "Type": "Log",
            "Name": "fluentd"
          },
... continues for >70 lines ...
```

</br>

## Get App Uptime Summary

### Usage:

```
<GET> http://placeholder.url/[SERVER_ID]/get-uptime-summary?name=[APP_NAME]&duration=[DURATION]
```

### Mode:

This method is compatible with both solo and swarm mode.

### Description:

Returns timestamped log data representing uptime since the duration specified in the parameter. Possible durations are "hour", "day", "week", or "month". Output is `true` if the app status is 'running', and `false` if it is anything else.

`SERVER_ID` - Server-specific identifier

`APP_NAME` - Server-specific identifier

`DURATION` - String to specify duration of log data to return. (must be "hour", "day", "week", or "month")

### Example Response:
``` json
{
  "2023-06-20T13:50:45": true,
  "2023-06-20T13:56:44": true,
  "2023-06-20T14:03:16": true,
  "2023-06-20T14:13:17": true,
  "2023-06-20T14:23:17": true,
  "2023-06-20T14:33:17": false,
  "2023-06-20T14:43:18": false
}
```

</br>

## Request Image

### Usage:

```
<POST> http://placeholder.url/[SERVER_ID]/request-image?image=[IMAGE_NAME]
```

### Mode:

This method is compatible with both solo and swarm mode.

### Description:

Request an image to be pulled from docker hub.

`SERVER_ID` - Server-specific identifier

`IMAGE_NAME` - Name of requested image

</br>

## Get Images

### Usage:

```
<GET> http://placeholder.url/[SERVER_ID]/get-images
```

### Mode:

This method is compatible with both solo and swarm mode.

### Description:

Returns an array of all existing images on the specified server. On top of the image information given by docker, another field called `CreatedContainerCount` will give the number of existing containers that were created from that image.

`SERVER_ID` - Server-specific identifier

### Example Response:
``` json
[
  {
    "Containers": "N/A",
    "CreatedAt": "2023-06-14 10:45:43 -1000 HST",
    "CreatedSince": "7 days ago",
    "Digest": "<none>",
    "ID": "ad303d7f80f9",
    "Repository": "httpd",
    "SharedSize": "N/A",
    "Size": "168MB",
    "Tag": "latest",
    "UniqueSize": "N/A",
    "VirtualSize": "168.1MB",
    "CreatedContainerCount": 2
  },
  {
    "Containers": "N/A",
    "CreatedAt": "2023-06-13 07:45:16 -1000 HST",
    "CreatedSince": "8 days ago",
    "Digest": "<none>",
    "ID": "09b1cac8826b",
    "Repository": "python",
    "SharedSize": "N/A",
    "Size": "1.01GB",
    "Tag": "latest",
    "UniqueSize": "N/A",
    "VirtualSize": "1.008GB",
    "CreatedContainerCount": 1
  }
]
```
