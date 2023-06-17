from flask import Flask, request, Response
import subprocess
import json

app = Flask(__name__)



@app.route('/<dsrc>/queryStatus')
def statusQuery(dsrc=""):
  """
  Returns basic information and status of the specified container.

  parameters:
    dsrc - this value is passed in the API route, for demo purposes this should always be mhpcc
    container_name - this value is passed as an http parameter

  returns:
    if successful, returns container information in json format
  """

  container_name = request.args.get("container")
  if container_name == None:
    return Response("No container name provided", status=400)

  if not _verifyDockerEngine():
    return Response("Docker daemon not responding", status=500)

  container_id = _getContainerID(container_name)
  if container_id == None:
    return Response(f"Unable to find app \"{container_name}\"", status=400)

  # this is temporary just for the demo
  if dsrc != "mhpcc":
    return Response("Invalid DSRC", status=400)

  # executing system command
  completedProcess = subprocess.run(f"docker ps -a -f id={container_id} --format json", capture_output=True)
  if completedProcess.returncode != 0:
    return Response(f"Failed to query app", status=500)

  output_list = completedProcess.stdout.decode().split("\n")
  output_list = map(json.loads, output_list)

  # docker ps returns a list of containers with matching names, so we must search
  # for the one that matches exactly
  for entry in output_list:
    if entry["Names"] == container_name:
      return Response(json.dumps(entry), status=200)

  return Response("This should not be reached", status=500)




@app.route('/<dsrc>/inspectContainer')
def inspectContainer(dsrc):
  """
  Returns detailed information of the specified container.

  parameters:
    dsrc - this value is passed in the API route, for demo purposes this should always be mhpcc
    container_name - this value is passed as an http parameter

  returns:
    if successful, returns container information in json format
  """
  container_name = request.args.get("container")
  if container_name == None:
    return Response("No container name provided", status=400)

  if not _verifyDockerEngine():
    return Response("Docker daemon not responding", status=500)

  container_id = _getContainerID(container_name)
  if container_id == None:
    return Response(f"Unable to find app \"{container_name}\"", status=400)

  # this is temporary just for the demo
  if dsrc != "mhpcc":
    return Response("Invalid DSRC", status=400)

  # executing system command
  completedProcess = subprocess.run(f"docker inspect --type=container {container_name}", capture_output=True)
  if completedProcess.returncode != 0:
    # undefined error
    return Response(f"Failed to inspect app", status=500)

  output_list = json.loads(completedProcess.stdout.decode())
  # docker inspect returns a list of containers, so we must search for the one
  # with a matching container name
  for entry in output_list:
    if entry["Name"].replace("/", "") == container_name:
      return Response(json.dumps(entry), status=200)

  return Response("", status=500)



@app.route('/<dsrc>/startContainer', methods=['POST'])
def startContainer(dsrc):
  """
  Sends a command to docker to start the specified container

  parameters:
    dsrc - this value is passed in the API route, for demo purposes this should always be mhpcc
    container_name - this value is passed as an http parameter
  """

  container_name = request.args.get("container")
  if container_name == None:
    return Response("No container name provided", status=400)

  if not _verifyDockerEngine():
    return Response("Docker daemon not responding", status=500)

  container_id = _getContainerID(container_name)
  if container_id == None:
    return Response(f"Unable to find app \"{container_name}\"", status=400)

  # this is temporary just for the demo
  if dsrc != "mhpcc":
    return Response("Invalid DSRC", status=400)

  # executing system command
  completedResponse = subprocess.run(f"docker start {container_name}", capture_output=True)
  if completedResponse.returncode != 0:
    return Response(f"Failed to start app", status=500)

  return Response("Success", status=200)


@app.route('/<dsrc>/stopContainer', methods=['POST'])
def stopContainer(dsrc):
  """
  Sends a command to docker to stop the specified container

  parameters:
    dsrc - this value is passed in the API route, for demo purposes this should always be mhpcc
    container_name - this value is passed as an http parameter
  """

  container_name = request.args.get("container")
  if container_name == None:
    return Response("No container name provided", status=400)

  if not _verifyDockerEngine():
    return Response("Docker daemon not responding", status=500)

  container_id = _getContainerID(container_name)
  if container_id == None:
    return Response(f"Unable to find app \"{container_name}\"", status=400)

  # this is temporary just for the demo
  if dsrc != "mhpcc":
    return Response("Invalid DSRC", status=400)

  # executing system command
  completedResponse = subprocess.run(f"docker stop {container_name}", capture_output=True)
  if completedResponse.returncode != 0:
    return Response(f"Failed to stop app", status=500)

  return Response("Success", status=200)


@app.route('/<dsrc>/restartContainer', methods=['POST'])
def restartContainer(dsrc):
  """
  Sends a command to docker to restart the specified container

  parameters:
    dsrc - this value is passed in the API route, for demo purposes this should always be mhpcc
    container_name - this value is passed as an http parameter
  """

  container_name = request.args.get("container")
  if container_name == None:
    return Response("No container name provided", status=400)

  if not _verifyDockerEngine():
    return Response("Docker daemon not responding", status=500)

  container_id = _getContainerID(container_name)
  if container_id == None:
    return Response(f"Unable to find app \"{container_name}\"", status=400)

  # this is temporary just for the demo
  if dsrc != "mhpcc":
    return Response("Invalid DSRC", status=400)

  # executing system command
  completedResponse = subprocess.run(f"docker restart {container_name}", capture_output=True)
  if completedResponse.returncode != 0:
    return Response(f"Failed to restart app", status=500)

  return Response("Success", status=200)



@app.route('/<dsrc>/killContainer', methods=['POST'])
def killContainer(dsrc):
  """
  Sends a command to docker to restart the specified container

  parameters:
    dsrc - this value is passed in the API route, for demo purposes this should always be mhpcc
    container_name - this value is passed as an http parameter
  """

  container_name = request.args.get("container")
  if container_name == None:
    return Response("No container name provided", status=400)

  if not _verifyDockerEngine():
    return Response("Docker daemon not responding", status=500)

  container_id = _getContainerID(container_name)
  if container_id == None:
    return Response(f"Unable to find app \"{container_name}\"", status=400)

  # this is temporary just for the demo
  if dsrc != "mhpcc":
    return Response("Invalid DSRC", status=400)

  # executing system command
  completedResponse = subprocess.run(f"docker kill {container_name}", capture_output=True)
  if completedResponse.returncode != 0:
    return Response(f"Failed to kill app", status=500)

  return Response("Success", status=200)


def _getContainerID(container_name:str) -> str | None:
  """
  this helper function that returns the id of the container matching the given name
  Returns None if unsuccessful
  """

  # executing system command
  completedResponse = subprocess.run(f"docker ps -a --filter name={container_name} --format \"{{{{.Names}}}} {{{{.ID}}}}\"", capture_output=True)
  if completedResponse.returncode != 0: return None

  if completedResponse.stdout == b'': return None

  # make list of names and ids
  nameList = [tuple(line.split()) for line in completedResponse.stdout.decode().split("\n")]
  print(nameList)
  # check if container_name is in list
  for name, id in nameList:
    if name == container_name:
      return id

  return None


def _verifyDockerEngine() -> bool:
  """
  This helper function verifies that the docker daemon is running
  """
  completedResponse = subprocess.run("docker ps", capture_output=True)
  return completedResponse.returncode == 0


if __name__ == '__main__':
  print("\n\n\n")
  app.run()