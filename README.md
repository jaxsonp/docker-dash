# SRC Container API

### Made by Jaxson Pahukula and Jayden Pahukula

_\[Updated 6/20]_

---

This API can be used to control and access information about containers running on SRC (Supercomputing Research Center) servers. Each method uses the app name to specify the container, so this name should match the container name exactly. Names should also follow the naming convention in order to work properly with Docker.

### Naming Convention

Because containers are identified by name, it is important that each container name is unique. Container names must only contain letters, numbers, dashes, and/or underscores.

### Error Handling

Each method performs checks in the same order. First, it checks if a name was provided, then it checks if the facility ID was provided and is valid. Next, it checks if the docker engine is online by running a `docker ps` command. Finally it checks if a container with the given name exists, and if so, starts with the actual job.

### Facility ID

Each facility will be identified by a unique key in order to specify which SRC to interface with. For demo purposes, this API only responds to a placeholder facility with the ID "demo".

---

# Get Container Status

### Usage:

``` plaintext
https://placeholder.url/[FACILITY_ID]/queryStatus?container=[CONTAINER_NAME]

```

### Description:

Returns basic information and status of specified container, in json format. Under the hood, this method makes use the `docker ps` commmand.  
`FACILITY_ID` - Facility-specific identifier  
`CONTAINER_NAME` - Name of container to query, must follow naming convention (specified above).

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

# Get container information

### Usage:

``` plaintext
https://placeholder.url/[FACILITY_ID]/inspectContainer?container=[CONTAINER_NAME]

```

### Description:

Returns detailed information of specified container, in json format. Under the hood, this method makes use the `docker inspect` commmand.  
`FACILITY_ID` - Facility-specific identifier  
`CONTAINER_NAME` - Name of container to query, must follow naming convention (specified above).

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
    "EndpointID": "7587b82f0dada3656fda26588aee72630c6fab1536d36e394b2bfbcf898c971d",
    "Gateway": "172.17.0.1",
    "GlobalIPv6Address": "",
    "GlobalIPv6PrefixLen": 0,
    "IPAddress": "172.17.0.2",
    "IPPrefixLen": 16,
    "IPv6Gateway": "",
    "MacAddress": "02:42:ac:12:00:02",
    "Networks": {
      "bridge": {
        "NetworkID": "7ea29fc1412292a2d7bba362f9253545fecdfa8ce9a6e37dd10ba8bee7129812",
        "EndpointID": "7587b82f0dada3656fda26588aee72630c6fab1536d36e394b2bfbcf898c971d",
        "Gateway": "172.17.0.1",
        "IPAddress": "172.17.0.2",
        "IPPrefixLen": 16,
        "IPv6Gateway": "",
        "GlobalIPv6Address": "",
        "GlobalIPv6PrefixLen": 0,
        "MacAddress": "02:42:ac:12:00:02"
      }
    }
  },
  "ResolvConfPath": "/var/lib/docker/containers/d2cc496561d6d520cbc0236b4ba88c362c446a7619992123f11c809cded25b47/resolv.conf",
  "HostnamePath": "/var/lib/docker/containers/d2cc496561d6d520cbc0236b4ba88c362c446a7619992123f11c809cded25b47/hostname",
  "HostsPath": "/var/lib/docker/containers/d2cc496561d6d520cbc0236b4ba88c362c446a7619992123f11c809cded25b47/hosts",
  "LogPath": "/var/lib/docker/containers/d2cc496561d6d520cbc0236b4ba88c362c446a7619992123f11c809cded25b47/d2cc496561d6d520cbc0236b4ba88c362c446a7619992123f11c809cded25b47-json.log",
  "Name": "/adoring_wozniak",
  "RestartCount": 0,
  "Driver": "devicemapper",
  "MountLabel": "",
  "ProcessLabel": "",
  "Mounts": [
    {
      "Source": "/data",
      "Destination": "/data",
      "Mode": "ro,Z",
      "RW": false,
      "Propagation": ""
    }
  ],
  "AppArmorProfile": "",
  "ExecIDs": null,
  "HostConfig": {
    "Binds": null,
    "ContainerIDFile": "",
    "Memory": 0,
    "MemorySwap": 0,
    "CpuShares": 0,
    "CpuPeriod": 0,
    "CpusetCpus": "",
    "CpusetMems": "",
    "CpuQuota": 0,
    "BlkioWeight": 0,
    "OomKillDisable": false,
    "Privileged": false,
    "PortBindings": {},
    "Links": null,
    "PublishAllPorts": false,
    "Dns": null,
    "DnsSearch": null,
    "DnsOptions": null,
    "ExtraHosts": null,
    "VolumesFrom": null,
    "Devices": [],
    "NetworkMode": "bridge",
    "IpcMode": "",
    "PidMode": "",
    "UTSMode": "",
    "CapAdd": null,
    "CapDrop": null,
    "RestartPolicy": {
      "Name": "no",
      "MaximumRetryCount": 0
    },
    "SecurityOpt": null,
    "ReadonlyRootfs": false,
    "Ulimits": null,
    "LogConfig": {
      "Type": "json-file",
      "Config": {}
    },
    "CgroupParent": ""
  },
  "GraphDriver": {
    "Name": "devicemapper",
    "Data": {
      "DeviceId": "5",
      "DeviceName": "docker-253:1-2763198-d2cc496561d6d520cbc0236b4ba88c362c446a7619992123f11c809cded25b47",
      "DeviceSize": "171798691840"
    }
  },
  "Config": {
    "Hostname": "d2cc496561d6",
    "Domainname": "",
    "User": "",
    "AttachStdin": true,
    "AttachStdout": true,
    "AttachStderr": true,
    "ExposedPorts": null,
    "Tty": true,
    "OpenStdin": true,
    "StdinOnce": true,
    "Env": null,
    "Cmd": [
      "bash"
    ],
    "Image": "fedora",
    "Volumes": null,
    "VolumeDriver": "",
    "WorkingDir": "",
    "Entrypoint": null,
    "NetworkDisabled": false,
    "MacAddress": "",
    "OnBuild": null,
    "Labels": {},
    "Memory": 0,
    "MemorySwap": 0,
    "CpuShares": 0,
    "Cpuset": "",
    "StopSignal": "SIGTERM"
  }
}

```

---

# Start container

### Usage:

``` plaintext
https://placeholder.url/[FACILITY_ID]/startContainer?container=[CONTAINER_NAME]

```

### Description:

Starts the specified container using the `docker start` command.

`FACILITY_ID` - Facility-specific identifier

`CONTAINER_NAME` - Name of container to start, must follow naming convention (specified above).

---

# Stop container

### Usage:

``` plaintext
https://placeholder.url/[FACILITY_ID]/stopContainer?container=[CONTAINER_NAME]

```

### Description:

Signals for the specified container to exit using the `docker stop` command. If the container does not exit within a 10 second grace period, it will kill the container forcefully.

`FACILITY_ID` - Facility-specific identifier

`CONTAINER_NAME` - Name of container to stop, must follow naming convention (specified above).

---

# Restart container

### Usage:

``` plaintext
https://placeholder.url/[FACILITY_ID]/restartContainer?container=[CONTAINER_NAME]

```

### Description:

Restarts the specified container using the `docker restart` command.

`FACILITY_ID` - Facility-specific identifier

`CONTAINER_NAME` - Name of container to restart, must follow naming convention (specified above).

---

# Kill container

### Usage:

``` plaintext
https://placeholder.url/[FACILITY_ID]/killContainer?container=[CONTAINER_NAME]

```

### Description:

Kills the specified container by sending it a `SIGKILL` signal using the `docker kill` command.

`FACILITY_ID` - Facility-specific identifier

`CONTAINER_NAME` - Name of container to kill, must follow naming convention (specified above).

---

# Get container names

### Usage:

``` plaintext
https://placeholder.url/[FACILITY_ID]/getContainers

```

### Description:

Returns an array of all containers on the specified DSRC, regardless of its status (e.g. running, exited)

`FACILITY_ID` - Facility-specific identifier

### Example Response:

``` json
["jupyter-lab", "xterm"]

```

---

# Get container health summary

### Usage:

``` plaintext
https://placeholder.url/[FACILITY_ID]/getHealthSummary?container=[CONTAINER_NAME]&duration=[DURATION]

```

### Description:

Returns timestamped log data representing uptime since the duration specified in the parameter. Possible durations are "hour", "day", "week", or "month".

`FACILITY_ID` - Facility-specific identifier

`CONTAINER_NAME` - Facility-specific identifier

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
