from flask import Flask, request, Response
import subprocess
import json
import threading

from internal_methods import *
from logger import loggingThreadFunc, getHealthSummary

app = Flask(__name__)


@app.route('/<facility_id>/getAppStatus')
@verifyFacilityID
@verifyDockerEngine
@verifyAppName
def getAppStatus(facility_id, app_name="", app_id="") -> Response:
  """
  Returns basic information and status of the specified app.

  parameters:
    facility_id - this value is passed in the API route, for demo purposes this should always be "demo"
    app_name - this value is passed as an http parameter

  returns:
    if successful, returns app information in json format
  """

  # executing system command
  completedProcess = subprocess.run(f"docker ps -a -f id={app_id} --format json", capture_output=True)
  if completedProcess.returncode != 0:
    return Response(f"Failed to query app", status=500)

  output_list = completedProcess.stdout.decode().split("\n")
  output_list = map(json.loads, output_list)

  # docker ps returns a list of containers with matching names, so we must search
  # for the one that matches exactly
  for entry in output_list:
    if entry["Names"] == app_name:
      return Response(json.dumps(entry), status=200)

  return Response("This should not be reached", status=500)




@app.route('/<facility_id>/getAppInfo')
@verifyFacilityID
@verifyDockerEngine
@verifyAppName
def getAppInfo(facility_id, app_name="", app_id="") -> Response:
  """
  Returns detailed information of the specified app.

  parameters:
    facility_id - this value is passed in the API route, for demo purposes this should always be "demo"
    app_name - this value is passed as an http parameter

  returns:
    if successful, returns app information in json format
  """

  # executing system command
  completedProcess = subprocess.run(f"docker inspect --type=container {app_id}", capture_output=True)
  if completedProcess.returncode != 0:
    # undefined error
    return Response(f"Failed to inspect app", status=500)

  output_list = json.loads(completedProcess.stdout.decode())
  # docker inspect returns a list of containers, so we must search for the one
  # with a matching app name
  for entry in output_list:
    if entry["Name"].replace("/", "") == app_name:
      return Response(json.dumps(entry), status=200)




@app.route('/<facility_id>/startApp', methods=['POST'])
@verifyFacilityID
@verifyDockerEngine
@verifyAppName
def startApp(facility_id, app_name="", app_id="") -> Response:
  """
  Sends a command to docker to start the specified app

  parameters:
    facility_id - this value is passed in the API route, for demo purposes this should always be "demo"
    app_name - this value is passed as an http parameter
  """

  # verify that app is not paused
  completedResponse = subprocess.run(f"docker ps -a -f id={app_id} --format \"{{{{.State}}}}\"", capture_output=True)
  if completedResponse.stdout.decode() == "paused\n":
    return Response("App is paused", status=409)

  # executing system command
  completedResponse = subprocess.run(f"docker start {app_id}", capture_output=True)
  if completedResponse.returncode != 0:
    return Response(f"Failed to start app", status=500)

  return Response("Success", status=200)




@app.route('/<facility_id>/stopApp', methods=['POST'])
@verifyFacilityID
@verifyDockerEngine
@verifyAppName
def stopApp(facility_id, app_name="", app_id="") -> Response:
  """
  Sends a command to docker to stop the specified app

  parameters:
    facility_id - this value is passed in the API route, for demo purposes this should always be "demo"
    app_name - this value is passed as an http parameter
  """

  # executing system command
  completedResponse = subprocess.run(f"docker stop {app_id}", capture_output=True)
  if completedResponse.returncode != 0:
    return Response(f"Failed to stop app", status=500)

  return Response("Success", status=200)




@app.route('/<facility_id>/pauseApp', methods=['POST'])
@verifyFacilityID
@verifyDockerEngine
@verifyAppName
def pauseApp(facility_id, app_name="", app_id="") -> Response:
  """
  Sends a command to docker to pause the specified app

  parameters:
    facility_id - this value is passed in the API route, for demo purposes this should always be "demo"
    app_name - this value is passed as an http parameter
  """

  # verify that app is running
  completedResponse = subprocess.run(f"docker ps -a -f id={app_id} --format \"{{{{.State}}}}\"", capture_output=True)
  if completedResponse.stdout.decode() != "running\n":
    return Response("App must be running to be paused", status=409)

  # executing system command
  completedResponse = subprocess.run(f"docker pause {app_id}", capture_output=True)
  if completedResponse.returncode != 0:
    return Response(f"Failed to pause app", status=500)

  return Response("Success", status=200)




@app.route('/<facility_id>/unpauseApp', methods=['POST'])
@verifyFacilityID
@verifyDockerEngine
@verifyAppName
def unpauseApp(facility_id, app_name="", app_id="") -> Response:
  """
  Sends a command to docker to unpause the specified app

  parameters:
    facility_id - this value is passed in the API route, for demo purposes this should always be "demo"
    app_name - this value is passed as an http parameter
  """

  # verify that app is running
  completedResponse = subprocess.run(f"docker ps -a -f id={app_id} --format \"{{{{.State}}}}\"", capture_output=True)
  if completedResponse.stdout.decode() != "paused\n":
    return Response("App must be paused to be unpaused", status=409)

  # executing system command
  completedResponse = subprocess.run(f"docker unpause {app_id}", capture_output=True)
  if completedResponse.returncode != 0:
    return Response(f"Failed to stop app", status=500)

  return Response("Success", status=200)




@app.route('/<facility_id>/restartApp', methods=['POST'])
@verifyFacilityID
@verifyDockerEngine
@verifyAppName
def restartApp(facility_id, app_name="", app_id="") -> Response:
  """
  Sends a command to docker to restart the specified app

  parameters:
    facility_id - this value is passed in the API route, for demo purposes this should always be "demo"
    app_name - this value is passed as an http parameter
  """

  # executing system command
  completedResponse = subprocess.run(f"docker restart {app_id}", capture_output=True)
  if completedResponse.returncode != 0:
    return Response(f"Failed to restart app", status=500)

  return Response("Success", status=200)




@app.route('/<facility_id>/killApp', methods=['POST'])
@verifyFacilityID
@verifyDockerEngine
@verifyAppName
def killApp(facility_id, app_name="", app_id="") -> Response:
  """
  Sends a command to docker to restart the specified app

  parameters:
    facility_id - this value is passed in the API route, for demo purposes this should always be "demo"
    app_name - this value is passed as an http parameter
  """

  # executing system command
  completedResponse = subprocess.run(f"docker kill {app_id}", capture_output=True)
  if completedResponse.returncode != 0:
    return Response("Failed to kill app", status=500)

  return Response("Success", status=200)




@app.route('/<facility_id>/getAppNames')
@verifyFacilityID
@verifyDockerEngine
def getAppNames(facility_id) -> Response:
  """
  Returns an array of all apps, running or not

  parameters:
    facility_id - this value is passed in the API route, for demo purposes this should always be "demo"
  """

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
@verifyFacilityID
@verifyDockerEngine
@verifyAppName
def getHealthSummaryWrapper(facility_id, app_name="", app_id="") -> Response:
  """
  Returns a summary of the health/uptime of an app

  parameters:
    facility_id - this value is passed in the API route, for demo purposes this should always be "demo"
    app_name - this value is passed as an http parameter
    duration - this value is passed as an http parameter to specify duration of
      log data to return. (hour, day, week, or month)

  returns:
    returns a timestamped list of bools representing uptime
  """

  duration = request.args.get("duration")
  if duration == None:
    return Response("No summary duration provided", status=400)

  if duration not in ["hour", "day", "week", "month"]:
    return Response("Invalid duration", status=400)

  # getting summary from logger
  output = getHealthSummary(app_name, duration)
  if output == None:
    return Response(f"Could not find log for \"{app_name}\"", status=400)
  return Response(json.dumps(output), 200)




if __name__ == '__main__':
  print("\n\n\n")

  print("Starting logging thread")
  logThread = threading.Thread(target=loggingThreadFunc, daemon=True)
  logThread.start()
  print("Starting flask server")
  app.run()