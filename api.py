from flask import Flask, request, Response
import subprocess
import json
import threading

from logger import loggingThreadFunc, getHealthSummary

app = Flask(__name__)



@app.route('/<facility_id>/queryStatus')
def statusQuery(facility_id) -> Response:
  """
  Returns basic information and status of the specified container.

  parameters:
    facility_id - this value is passed in the API route, for demo purposes this should always be "demo"
    container_name - this value is passed as an http parameter

  returns:
    if successful, returns container information in json format
  """

  container_name = request.args.get("container")
  if container_name == None:
    return Response("No container name provided", status=400)

  # this is temporary just for the demo
  if facility_id != "demo":
    return Response("Invalid facility ID", status=400)

  if not _verifyDockerEngine():
    return Response("Docker daemon not responding", status=500)

  container_id = _getContainerID(container_name)
  if container_id == None:
    return Response(f"Unable to find app \"{container_name}\"", status=400)

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




@app.route('/<facility_id>/inspectContainer')
def inspectContainer(facility_id) -> Response:
  """
  Returns detailed information of the specified container.

  parameters:
    facility_id - this value is passed in the API route, for demo purposes this should always be "demo"
    container_name - this value is passed as an http parameter

  returns:
    if successful, returns container information in json format
  """
  container_name = request.args.get("container")
  if container_name == None:
    return Response("No container name provided", status=400)

  # this is temporary just for the demo
  if facility_id != "demo":
    return Response("Invalid facility ID", status=400)

  if not _verifyDockerEngine():
    return Response("Docker daemon not responding", status=500)

  container_id = _getContainerID(container_name)
  if container_id == None:
    return Response(f"Unable to find app \"{container_name}\"", status=400)

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




@app.route('/<facility_id>/startContainer', methods=['POST'])
def startContainer(facility_id) -> Response:
  """
  Sends a command to docker to start the specified container

  parameters:
    facility_id - this value is passed in the API route, for demo purposes this should always be "demo"
    container_name - this value is passed as an http parameter
  """

  container_name = request.args.get("container")
  if container_name == None:
    return Response("No container name provided", status=400)

  # this is temporary just for the demo
  if facility_id != "demo":
    return Response("Invalid facility ID", status=400)

  if not _verifyDockerEngine():
    return Response("Docker daemon not responding", status=500)

  container_id = _getContainerID(container_name)
  if container_id == None:
    return Response(f"Unable to find app \"{container_name}\"", status=400)
  
  # verify that container is not paused
  completedResponse = subprocess.run(f"docker ps -a -f id={container_id} --format \"{{{{.State}}}}\"", capture_output=True)
  if completedResponse.stdout.decode() == "paused\n":
    return Response("Container is paused", status=409)

  # executing system command
  completedResponse = subprocess.run(f"docker start {container_name}", capture_output=True)
  if completedResponse.returncode != 0:
    return Response(f"Failed to start app", status=500)

  return Response("Success", status=200)




@app.route('/<facility_id>/stopContainer', methods=['POST'])
def stopContainer(facility_id) -> Response:
  """
  Sends a command to docker to stop the specified container

  parameters:
    facility_id - this value is passed in the API route, for demo purposes this should always be "demo"
    container_name - this value is passed as an http parameter
  """

  container_name = request.args.get("container")
  if container_name == None:
    return Response("No container name provided", status=400)

  # this is temporary just for the demo
  if facility_id != "demo":
    return Response("Invalid facility ID", status=400)

  if not _verifyDockerEngine():
    return Response("Docker daemon not responding", status=500)

  container_id = _getContainerID(container_name)
  if container_id == None:
    return Response(f"Unable to find app \"{container_name}\"", status=400)

  # executing system command
  completedResponse = subprocess.run(f"docker stop {container_name}", capture_output=True)
  if completedResponse.returncode != 0:
    return Response(f"Failed to stop app", status=500)

  return Response("Success", status=200)




@app.route('/<facility_id>/pauseContainer', methods=['POST'])
def pauseContainer(facility_id) -> Response:
  """
  Sends a command to docker to pause the specified container

  parameters:
    facility_id - this value is passed in the API route, for demo purposes this should always be "demo"
    container_name - this value is passed as an http parameter
  """

  container_name = request.args.get("container")
  if container_name == None:
    return Response("No container name provided", status=400)

  # this is temporary just for the demo
  if facility_id != "demo":
    return Response("Invalid facility ID", status=400)

  if not _verifyDockerEngine():
    return Response("Docker daemon not responding", status=500)

  container_id = _getContainerID(container_name)
  if container_id == None:
    return Response(f"Unable to find app \"{container_name}\"", status=400)

  # verify that container is running
  completedResponse = subprocess.run(f"docker ps -a -f id={container_id} --format \"{{{{.State}}}}\"", capture_output=True)
  if completedResponse.stdout.decode() != "running\n":
    return Response("Container must be running to be paused", status=409)

  # executing system command
  completedResponse = subprocess.run(f"docker pause {container_name}", capture_output=True)
  if completedResponse.returncode != 0:
    return Response(f"Failed to pause app", status=500)

  return Response("Success", status=200)




@app.route('/<facility_id>/unpauseContainer', methods=['POST'])
def unpauseContainer(facility_id) -> Response:
  """
  Sends a command to docker to unpause the specified container

  parameters:
    facility_id - this value is passed in the API route, for demo purposes this should always be "demo"
    container_name - this value is passed as an http parameter
  """

  container_name = request.args.get("container")
  if container_name == None:
    return Response("No container name provided", status=400)

  # this is temporary just for the demo
  if facility_id != "demo":
    return Response("Invalid facility ID", status=400)

  if not _verifyDockerEngine():
    return Response("Docker daemon not responding", status=500)

  container_id = _getContainerID(container_name)
  if container_id == None:
    return Response(f"Unable to find app \"{container_name}\"", status=400)

  # verify that container is running
  completedResponse = subprocess.run(f"docker ps -a -f id={container_id} --format \"{{{{.State}}}}\"", capture_output=True)
  if completedResponse.stdout.decode() != "paused\n":
    return Response("Container must be paused to be unpaused", status=409)

  # executing system command
  completedResponse = subprocess.run(f"docker unpause {container_name}", capture_output=True)
  if completedResponse.returncode != 0:
    return Response(f"Failed to stop app", status=500)

  return Response("Success", status=200)




@app.route('/<facility_id>/restartContainer', methods=['POST'])
def restartContainer(facility_id) -> Response:
  """
  Sends a command to docker to restart the specified container

  parameters:
    facility_id - this value is passed in the API route, for demo purposes this should always be "demo"
    container_name - this value is passed as an http parameter
  """

  container_name = request.args.get("container")
  if container_name == None:
    return Response("No container name provided", status=400)

  # this is temporary just for the demo
  if facility_id != "demo":
    return Response("Invalid facility ID", status=400)

  if not _verifyDockerEngine():
    return Response("Docker daemon not responding", status=500)

  container_id = _getContainerID(container_name)
  if container_id == None:
    return Response(f"Unable to find app \"{container_name}\"", status=400)

  # executing system command
  completedResponse = subprocess.run(f"docker restart {container_name}", capture_output=True)
  if completedResponse.returncode != 0:
    return Response(f"Failed to restart app", status=500)

  return Response("Success", status=200)




@app.route('/<facility_id>/killContainer', methods=['POST'])
def killContainer(facility_id) -> Response:
  """
  Sends a command to docker to restart the specified container

  parameters:
    facility_id - this value is passed in the API route, for demo purposes this should always be "demo"
    container_name - this value is passed as an http parameter
  """

  container_name = request.args.get("container")
  if container_name == None:
    return Response("No container name provided", status=400)

  # this is temporary just for the demo
  if facility_id != "demo":
    return Response("Invalid facility ID", status=400)

  if not _verifyDockerEngine():
    return Response("Docker daemon not responding", status=500)

  container_id = _getContainerID(container_name)
  if container_id == None:
    return Response(f"Unable to find app \"{container_name}\"", status=400)

  # executing system command
  completedResponse = subprocess.run(f"docker kill {container_name}", capture_output=True)
  if completedResponse.returncode != 0:
    return Response("Failed to kill app", status=500)

  return Response("Success", status=200)




@app.route('/<facility_id>/getContainers')
def getContainers(facility_id) -> Response:
  """
  Returns an array of all containers, running or not

  parameters:
    facility_id - this value is passed in the API route, for demo purposes this should always be "demo"
  """

  # this is temporary just for the demo
  if facility_id != "demo":
    return Response("Invalid facility ID", status=400)

  if not _verifyDockerEngine():
    return Response("Docker daemon not responding", status=500)

  # executing system command
  completedResponse = subprocess.run(f"docker ps -a --format \"{{{{.Names}}}}\"", capture_output=True)
  if completedResponse.returncode != 0:
    return Response("Unknown error", status=500)

  arr = []
  for string in completedResponse.stdout.decode().split("\n"):
    if string != "":
      arr.append(string)

  return Response(json.dumps(arr), 200)




@app.route('/<facility_id>/getHealthSummary')
def getHealthSummaryWrapper(facility_id) -> Response:
  """
  Returns an array of all containers, running or not

  parameters:
    facility_id - this value is passed in the API route, for demo purposes this should always be "demo"
  """

  container_name = request.args.get("container")
  if container_name == None:
    return Response("No container name provided", status=400)

  duration = request.args.get("duration")
  if duration == None:
    return Response("No summary duration provided", status=400)

  if duration not in ["hour", "day", "week", "month"]:
    return Response("Invalid duration", status=400)

  # this is temporary just for the demo
  if facility_id != "demo":
    return Response("Invalid facility ID", status=400)

  if not _verifyDockerEngine():
    return Response("Docker daemon not responding", status=500)

  # getting summary from logger
  output = getHealthSummary(container_name, duration)
  if output == None:
    return Response(f"Could not find log for \"{container_name}\"", status=400)
  return Response(json.dumps(output), 200)





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

  print("Starting logging thread")
  logThread = threading.Thread(target=loggingThreadFunc, daemon=True)
  logThread.start()
  print("Starting flask server")
  app.run()