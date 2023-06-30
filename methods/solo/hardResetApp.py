import flask
from methods import internal_methods

@internal_methods.verifyFacilityID
@internal_methods.verifyDockerEngine(swarm_method=False)
@internal_methods.handleAppName
def hardResetApp(facility_id, app_name="", app_id="") -> flask.Response:
  """
  This method deletes then re-creates a container, clearing all data

  parameters:
    facility_id - this value is passed in the API route, for demo purposes this should always be "demo"
    app_name - this value is passed as an http parameter
  """

  completedProcess = internal_methods.subprocessRun(f"docker inspect {app_name} --format \"{{{{.Config.Image}}}}\"")
  image_name = completedProcess.stdout.decode().strip()

  # stopping container
  internal_methods.subprocessRun(f"docker stop {app_id}")
  # deleting container
  completedProcess = internal_methods.subprocessRun(f"docker rm {app_id}")
  if completedProcess.returncode != 0:
    return flask.make_response("Failed to delete app:\n"+completedProcess.stdout.decode()+"\n"+completedProcess.stderr.decode(), 500)

  # re-creating container
  completedProcess = internal_methods.subprocessRun(f"docker create --name \"{app_name}\" --pull never \"{image_name}\"")
  if completedProcess.returncode != 0:
    return flask.make_response("Failed to create app:\n"+completedProcess.stdout.decode()+"\n"+completedProcess.stderr.decode(), 500)

  return flask.make_response("Success", 200)