import flask
from methods import internal_methods

@internal_methods.verifyServerID
@internal_methods.verifyDockerEngine(swarm_method=False)
@internal_methods.handleAppName
def soloHardResetApp(server_id, app_name="", app_id="") -> flask.Response:
  """
  This method deletes then re-creates a container, clearing all data

  parameters:
    server_id - this value is passed in the API route, for demo purposes this should always be "demo"
    app_name - this value is passed as an http parameter
    app_id - this value is obtained when the app_name is verified with the handleAppName decorator
  """

  # get original image name
  completedProcess = internal_methods.subprocessRun(f"docker inspect {app_name} --format \"{{{{.Config.Image}}}}\"")
  image_name = completedProcess.stdout.decode().strip()

  # stop container
  internal_methods.subprocessRun(f"docker stop {app_id}")
  # delete container
  completedProcess = internal_methods.subprocessRun(f"docker rm {app_id}")
  if completedProcess.returncode != 0:
    return flask.make_response("Failed to delete app:\n"+completedProcess.stdout.decode()+"\n"+completedProcess.stderr.decode(), 500)

  # re-create container
  completedProcess = internal_methods.subprocessRun(f"docker create --name \"{app_name}\" --pull never \"{image_name}\"")
  if completedProcess.returncode != 0:
    return flask.make_response("Failed to create app:\n"+completedProcess.stdout.decode()+"\n"+completedProcess.stderr.decode(), 500)

  return flask.make_response("Success", 200)