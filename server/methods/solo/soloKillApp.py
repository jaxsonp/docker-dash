import flask
from methods import internal_methods


@internal_methods.verifyServerID
@internal_methods.verifyDockerEngine(swarm_method=False)
@internal_methods.handleAppName
def soloKillApp(server_id, app_name="", app_id="") -> flask.Response:
  """
  Sends a command to docker to restart the specified app

  parameters:
    server_id - this value is passed in the API route, for demo purposes this should always be "demo"
    app_name - this value is passed as an http parameter
  """

  # executing system command
  completedProcess = internal_methods.subprocessRun(f"docker kill {app_id}")
  if completedProcess.returncode != 0:
    return flask.make_response("Failed to kill app:\n"+completedProcess.stdout.decode()+"\n"+completedProcess.stderr.decode(), 500)

  return flask.make_response("Success", 200)