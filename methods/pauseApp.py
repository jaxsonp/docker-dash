import subprocess
from flask import Response
from . import internal_methods


@internal_methods.verifyFacilityID
@internal_methods.verifyDockerEngine
@internal_methods.handleAppName
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