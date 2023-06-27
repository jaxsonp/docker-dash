import subprocess
import flask
from . import internal_methods


@internal_methods.verifyFacilityID
@internal_methods.verifyDockerEngine
@internal_methods.handleAppName
def unpauseApp(facility_id, app_name="", app_id="") -> flask.Response:
  """
  Sends a command to docker to unpause the specified app

  parameters:
    facility_id - this value is passed in the API route, for demo purposes this should always be "demo"
    app_name - this value is passed as an http parameter
  """

  # verify that app is running
  completedProcess = internal_methods.subprocessRun(f"docker ps -a -f id={app_id} --format \"{{{{.State}}}}\"", shell=True, capture_output=True)
  if completedProcess.stdout.decode() != "paused\n":
    return flask.make_response("App must be paused to be unpaused", 409)

  # executing system command
  completedProcess = internal_methods.subprocessRun(f"docker unpause {app_id}", shell=True, capture_output=True)
  if completedProcess.returncode != 0:
    return flask.make_response(f"Failed to stop app:\n"+completedProcess.stdout.decode()+"\n"+completedProcess.stderr.decode(), 500)

  return flask.make_response("Success", 200)