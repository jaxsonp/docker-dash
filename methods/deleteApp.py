import subprocess
import flask
from . import internal_methods


@internal_methods.verifyFacilityID
@internal_methods.verifyDockerEngine
@internal_methods.handleAppName
def deleteApp(facility_id, app_name="", app_id="") -> flask.Response:
  """
  This method stops and deletes a container

  parameters:
    facility_id - this value is passed in the API route, for demo purposes this should always be "demo"
    image - this value is passed as an http parameter
  """

  # executing system commands
  subprocess.run(f"docker stop \"{app_id}\"", shell=True, capture_output=True)
  completedProcess = subprocess.run(f"docker rm \"{app_id}\"", shell=True, capture_output=True)
  if completedProcess.returncode != 0:
    # uncaught error
    return flask.make_response("Failed to delete app:\n"+completedProcess.stdout.decode()+"\n"+completedProcess.stderr.decode(), 500)

  return flask.make_response("Success", 200)