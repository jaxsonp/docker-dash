import subprocess
import flask
from . import internal_methods


@internal_methods.verifyFacilityID
@internal_methods.verifyDockerEngine
@internal_methods.handleAppName
def restartApp(facility_id, app_name="", app_id="") -> flask.Response:
  """
  Sends a command to docker to restart the specified app

  parameters:
    facility_id - this value is passed in the API route, for demo purposes this should always be "demo"
    app_name - this value is passed as an http parameter
  """

  # executing system command
  completedResponse = subprocess.run(f"docker restart {app_id}", capture_output=True)
  if completedResponse.returncode != 0:
    return flask.make_response(f"Failed to restart app", 500)

  return flask.make_response("Success", 200)