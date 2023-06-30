import flask
from methods import internal_methods


@internal_methods.verifyFacilityID
@internal_methods.verifyDockerEngine(swarm_method=False)
@internal_methods.handleAppName
def deleteApp(facility_id, app_name="", app_id="") -> flask.Response:
  """
  This method stops and deletes a container

  parameters:
    facility_id - this value is passed in the API route, for demo purposes this should always be "demo"
    image - this value is passed as an http parameter
  """

  # executing system commands
  internal_methods.subprocessRun(f"docker stop \"{app_id}\"")
  completedProcess = internal_methods.subprocessRun(f"docker rm \"{app_id}\"")
  if completedProcess.returncode != 0:
    # uncaught error
    return flask.make_response("Failed to delete app:\n"+completedProcess.stdout.decode()+"\n"+completedProcess.stderr.decode(), 500)

  return flask.make_response("Success", 200)