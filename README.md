# DSRC Docker Container API
*Last updated 6/19/23*
This API can be used to control and access information about containers running on DSRC servers. Each method uses the name to specify the container, so this name should match the container name exactly. Names should also follow the naming convention in order to work properly with Docker.
### Naming Convention
Because containers are identified by name, it is important that each container name is unique. Container names must only contain letters, numbers, dashes, and/or underscores.
### Error Handling
Each method performs checks in the same order. First, it checks if a name was provided, then it checks if the DSRC key was provided and is valid. Next, it checks if the docker daemon is online by running a docker ps command. Finally it checks if a container with the given name exists, and if so, starts with the actual job.
### DSRC Key
Each DSRC will be identified by a unique key, but the only one that works for now for demo purposes is `mhpcc`.

---
# Get Container Information
### Usage:
`https://placeholder.url/[DSRC_KEY]/queryStatus?container=[CONTAINER_NAME]`
### Description:
Returns basic information and status of specified container, in json format. Under the hood, this method makes use the docker ps commmand.
- DSRC_KEY - DSRC-specific identifier
- CONTAINER_NAME - Name of container to query, must follow naming convention (specified above).
### Example Response:
```json
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
# Get container information
### Usage:
`https://placeholder.url/[DSRC_KEY]/inspectContainer?container=[CONTAINER_NAME]`
### Description:
Returns detailed information of specified container, in json format. Under the hood, this method makes use the docker inspect commmand.
- DSRC_KEY - DSRC-specific identifier
- CONTAINER_NAME - Name of container to query, must follow naming convention (specified above).
### Example Response:
```json
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
   
... continues for >100 lines ...
```

---
# Start container
### Usage:
`https://placeholder.url/[DSRC_KEY]/startContainer?container=[CONTAINER_NAME]`
### Description:
Starts the specified container using the docker start command.
- DSRC_KEY - DSRC-specific identifier
- CONTAINER_NAME - Name of container to start, must follow naming convention (specified above).

---
# Stop container
### Usage:
`https://placeholder.url/[DSRC_KEY]/stopContainer?container=[CONTAINER_NAME]`
### Description:
Stops the specified container using the docker stop command.
- DSRC_KEY - DSRC-specific identifier
- CONTAINER_NAME - Name of container to stop, must follow naming convention (specified above).

---
# Restart container
### Usage:
`https://placeholder.url/[DSRC_KEY]/restartContainer?container=[CONTAINER_NAME]`
### Description:
Restarts the specified container using the docker restart command.
- DSRC_KEY - DSRC-specific identifier
- CONTAINER_NAME - Name of container to restart, must follow naming convention (specified above).

---
# Kill container
### Usage:
`https://placeholder.url/[DSRC_KEY]/killContainer?container=[CONTAINER_NAME]`


### Description:
Kills the specified container by sending it a SIGKILL signal using the docker kill command.
- DSRC_KEY - DSRC-specific identifier
- CONTAINER_NAME - Name of container to kill, must follow naming convention (specified above).
