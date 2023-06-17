from flask import Flask, request, Response
import subprocess
import json

app = Flask(__name__)


@app.route('/<dsrc>/queryStatus')
def statusQuery(dsrc):
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

  container_id = _verifyContainer(container_name)
  if container_id == None:
    return Response(f"Unable to find app: {container_name}", status=400)

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

  # this is temporary just for the demo
  if dsrc != "mhpcc":
    return Response("Invalid DSRC", status=400)

  # executing system command
  completedProcess = subprocess.run(f"docker inspect --type=container {container_name}", capture_output=True)
  if completedProcess.returncode != 0:
    if completedProcess.stdout == b'[]\n':
      # no matching container found
      return Response(f"Unable to find app: {container_name}", status=400)

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

  """

  container_name = request.args.get("container")
  if container_name == None:
    return Response("No container name provided", status=400)

  # executing system command
  completedResponse = subprocess.run(f"docker start {container_name}", capture_output=True)
  if completedResponse.returncode != 0:
    return Response(f"Failed to start app", status=500)

  return Response("Success", status=200)




def _getContainerID(container_name:str):
  """
  A helper function that returns the id of 
  """

  # executing system command
  completedResponse = subprocess.run(f"docker ps -a --filter name={container_name} --format \"{{{{.Names .ID}}}}\"")
  if completedResponse.returncode != 0: return None

  # make list of names and ids
  nameList = [tuple(line.split()) for line in completedResponse.stdout.decode().split("\n")]

  # check if container_name is in list
  for name, id in nameList:
    if name == container_name:
      return id

  return None




if __name__ == '__main__':
  print("\n\n\n")
  app.run()