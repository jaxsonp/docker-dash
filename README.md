# SRC Container API

This API can be used to control and access information about apps running as Docker containers on SRC (supercomputing research center) servers. Each method uses the app name to specify the container, so this name should match the container name exactly. Names should also follow the naming convention in order to work properly with Docker.

_Note: The words 'app' and 'container' both refer to the Docker container that the app is running on._

## Naming Convention

When an app is created, the image and user name are provided, then the container is made with the name `"image_name.user_name"`. All subsequent references to this container will use this name.

Names can include uppercase and lowercase letters and numbers, as well as dashes and underscores. The image name can use dots, but the last dot is used as a deliminator between image and user name, so the user name cannot have dots in it. Image names in docker hub are already unique, but user names must be unique as well.

## Facility ID

Each facility will be identified by a unique key in order to specify which SRC to interface with. For demo purposes, this API only responds to a placeholder facility with the ID "demo".

## Error Handling

Each method performs checks in the same order. First it checks if the facility ID was provided and is valid. Next, it checks if the docker engine is online by running a `docker ps` command. Finally it checks if an app name was provided and if it exists, and if so, starts with the actual job.

## API Endpoints:

1. [Start App](#start-app)
2. [Stop App](#stop-app)
3. [Pause App](#pause-app)
4. [Unpause App](#unpause-app)
5. [Restart App](#restart-app)
6. [Kill App](#kill-app)
7. [Create App](#create-app)
8. [Delete App](#delete-app)
9. [Hard Reset App](#hard-reset-app)
10. [Get App Names](#get-app-names)
11. [Get App Status](#get-app-status)
12. [Get App Stats](#get-app-stats)
13. [Get App Information](#get-app-information)
14. [Get App Health Summary](#get-app-health-summary)
15. [Request Image](#request-image)
16. [Get Images](#get-images)


---

# Start App

### Usage:

```
http://placeholder.url/[FACILITY_ID]/start-app?name=[APP_NAME]

```

### Description:

Starts the specified app using the `docker start` command. Trying to start an app that is paused will return an error, a paused app must be unpaused.

`FACILITY_ID` - Facility-specific identifier

`APP_NAME` - Name of app to start, must follow [naming convention](#naming-convention).

---

# Stop App

### Usage:

```
http://placeholder.url/[FACILITY_ID]/stop-app?name=[APP_NAME]

```

### Description:

Signals for the specified app to exit using the `docker stop` command. If the container does not respond to the `SIGTERM` signal within a 10 second grace period, it will kill the container forcefully with `SIGKILL`.

`FACILITY_ID` - Facility-specific identifier

`APP_NAME` - Name of app to stop, must follow [naming convention](#naming-convention).

---

# Pause App

### Usage:

```
http://placeholder.url/[FACILITY_ID]/pause-app?name=[APP_NAME]

```

### Description:

Pauses the specified app using the `docker pause` command. An app must be already running in order to be paused, otherwise the api will return error. While an app is paused, it can be unpaused, stopped, restarted, or killed.

`FACILITY_ID` - Facility-specific identifier

`APP_NAME` - Name of app to pause, must follow [naming convention](#naming-convention).

---

# Unpause App

### Usage:

```
http://placeholder.url/[FACILITY_ID]/unpause-app?name=[APP_NAME]

```

### Description:

Unpauses the specified app using the `docker unpause` command. An app must be paused, otherwise the api will return error.

`FACILITY_ID` - Facility-specific identifier

`APP_NAME` - Name of app to unpause, must follow [naming convention](#naming-convention).

---

# Restart App

### Usage:

```
http://placeholder.url/[FACILITY_ID]/restart-app?name=[APP_NAME]

```

### Description:

Restarts the specified app using the `docker restart` command. This command behaves similarly to a `docker stop` then a `docker start` command.

`FACILITY_ID` - Facility-specific identifier

`APP_NAME` - Name of app to restart, must follow [naming convention](#naming-convention).

---

# Kill App

### Usage:

```
http://placeholder.url/[FACILITY_ID]/kill-app?name=[APP_NAME]

```

### Description:

Kills the specified app by ending the relevant service, which removes all related data. Therefore, this method can be thought of as both killing and deleting.

`FACILITY_ID` - Facility-specific identifier

`APP_NAME` - Name of app to kill, must follow [naming convention](#naming-convention).

---

# Create App

### Usage:

```
http://placeholder.url/[FACILITY_ID]/create-app?image=[IMAGE_NAME]&user=[USER_NAME]

```

### Description:

Creates an app instance using the image specified. The image must have already been requested and approved in order to be used to create an app.

`FACILITY_ID` - Facility-specific identifier

`IMAGE_NAME` - Name of the image to load the app from

`USER_NAME` - Name of the user who is using the app

---

# Delete App

### Usage:

```
http://placeholder.url/[FACILITY_ID]/delete-app?name=[APP_NAME]

```

### Description:

Deletes the specified app, removing ALL related data.

`FACILITY_ID` - Facility-specific identifier

`APP_NAME` - Name of app to delete

---

# Hard Reset App

### Usage:

```
http://placeholder.url/[FACILITY_ID]/hard-reset-app?name=[APP_NAME]

```

### Description:

Resets the specified app, clearing ALL data and restoring it from the original image. Under the hood this method stops and deletes the app instance, then recreates it from the source image.

`FACILITY_ID` - Facility-specific identifier

`APP_NAME` - Name of app to reset

---

# Get App Names

### Usage:

```
http://placeholder.url/[FACILITY_ID]/get-app-names

```

### Description:

Returns an array of all existing apps on the specified SRC, regardless of its status (e.g. running, exited)

`FACILITY_ID` - Facility-specific identifier

### Example Response:

``` json
["jupyter-lab--jaxsonp", "xterm--admin"]

```

---

# Get App Status

### Usage:

```
http://placeholder.url/[FACILITY_ID]/get-app-status?name=[APP_NAME]

```

### Description:

Returns basic information and status, in json format. Under the hood, this method just returns the output of the `docker ps` commmand.

`FACILITY_ID` - Facility-specific identifier

`APP_NAME` **(Optional)**: Name of app to query, must follow [naming convention](#naming-convention). If omitted, will return a list of all apps and statuses.

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

---

# Get App Stats

### Usage:

```
http://placeholder.url/[FACILITY_ID]/get-app-stats?name=[APP_NAME]

```

### Description:

Returns hardware information in json format, using the `docker stats` commmand.

`FACILITY_ID` - Facility-specific identifier

`APP_NAME` **(Optional)**: Name of app to query, must follow [naming convention](#naming-convention). If omitted, will return a list of all apps and statuses.

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

---

# Get App Information

### Usage:

```
http://placeholder.url/[FACILITY_ID]/get-app-info?name=[APP_NAME]

```

### Description:

Returns detailed information of specified app, in json format. Under the hood, this method uses the `docker inspect` commmand.

`FACILITY_ID` - Facility-specific identifier

`APP_NAME` - Name of app to query, must follow [naming convention](#naming-convention).

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

---

# Get Uptime Summary

### Usage:

```
http://placeholder.url/[FACILITY_ID]/get-uptime-summary?name=[APP_NAME]&duration=[DURATION]

```

### Description:

Returns timestamped log data representing uptime since the duration specified in the parameter. Possible durations are "hour", "day", "week", or "month". Output is `true` if the app status is 'running', and `false` if it is anything else.

`FACILITY_ID` - Facility-specific identifier

`APP_NAME` - Facility-specific identifier

`DURATION` - String to specify duration of log data to return. (hour, day, week, or month)

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

---

# Request Image

### Usage:

```
http://placeholder.url/[FACILITY_ID]/request-image?image=[IMAGE_NAME]

```

### Description:

Request an image to be pulled from docker hub.

`FACILITY_ID` - Facility-specific identifier

`IMAGE_NAME` - Name of requested image

---

# Get Images

### Usage:

```
http://placeholder.url/[FACILITY_ID]/get-images

```

### Description:

Returns an array of all existing images on the specified SRC. On top of the image information given by docker, another field called `CreatedContainerCount` will give the number of existing containers that were created from that image.

`FACILITY_ID` - Facility-specific identifier

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