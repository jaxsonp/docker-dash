import flask
from methods import internal_methods


@internal_methods.verifyFacilityID
@internal_methods.verifyDockerEngine(swarm_method=False)
@internal_methods.handleAppName
def pauseApp(facility_id, app_name="", app_id="") -> flask.Response:
  """
  Sends a command to docker to pause the specified app

  parameters:
    facility_id - this value is passed in the API route, for demo purposes this should always be "demo"
    app_name - this value is passed as an http parameter
  """

  # verify that app is running
  completedProcess = internal_methods.subprocessRun(f"docker ps -a -f id={app_id} --format \"{{{{.State}}}}\"")
  if completedProcess.stdout.decode() != "running\n":
    return flask.make_response("App must be running to be paused", 409)

  # executing system command
  completedProcess = internal_methods.subprocessRun(f"docker pause {app_id}")
  if completedProcess.returncode != 0:
    return flask.make_response("Failed to pause app:\n"+completedProcess.stdout.decode()+"\n"+completedProcess.stderr.decode(), 500)

  return flask.make_response("Success", 200)