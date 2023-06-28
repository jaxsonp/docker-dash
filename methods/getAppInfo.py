import subprocess
import json
import flask
from . import internal_methods


@internal_methods.verifyFacilityID
@internal_methods.verifyDockerEngine
@internal_methods.handleAppName
def getAppInfo(facility_id, app_name="", app_id="") -> flask.Response:
  """
  Returns detailed information of the specified app.

  parameters:
    facility_id - this value is passed in the API route, for demo purposes this should always be "demo"
    app_name - this value is passed as an http parameter

  returns:
    if successful, returns app information in json format
  """

  # executing system command
  completedProcess = internal_methods.subprocessRun(f"docker inspect --type=container {app_id}", shell=True, capture_output=True)
  if completedProcess.returncode != 0:
    # undefined error
    return flask.make_response("Failed to inspect app:\n"+completedProcess.stdout.decode()+"\n"+completedProcess.stderr.decode(), 500)

  output_list = json.loads(completedProcess.stdout.decode())
  # docker inspect returns a list of containers, so we must search for the one
  # with a matching app name
  for entry in output_list:
    if entry["Name"].replace("/", "") == app_name:
      return flask.make_response(json.dumps(entry), 200)

  return flask.make_response("", 500)