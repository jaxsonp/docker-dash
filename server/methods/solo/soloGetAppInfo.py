import flask
import json
from methods import internal_methods

@internal_methods.verifyServerID
@internal_methods.verifyDockerEngine(swarm_method=False)
@internal_methods.handleAppName
def soloGetAppInfo(server_id, app_name="", app_id="") -> flask.Response:
  """
  Returns detailed information of the specified app.

  parameters:
    server_id - this value is passed in the API route, for demo purposes this should always be "demo"
    app_name - this value is passed as an http parameter
    app_id - this value is obtained when the app_name is verified with the handleAppName decorator

  returns:
    if successful, returns app information in json format
  """

  # executing docker command
  completedProcess = internal_methods.subprocessRun(f"docker inspect --type=container --format json {app_id}")
  if completedProcess.returncode != 0:
    # uncaught error
    return flask.make_response("Failed to inspect app:\n"+completedProcess.stdout.decode()+"\n"+completedProcess.stderr.decode(), 500)

  output_list = json.loads(completedProcess.stdout.decode())
  # docker inspect returns a list of containers, so we must search for the one with a matching app name
  for entry in output_list:
    if entry["Name"].replace("/", "") == app_name:
      return flask.make_response(json.dumps(entry), 200)

  return flask.make_response("Something went wrong with soloGetAppInfo.py", 500)