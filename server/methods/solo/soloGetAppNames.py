import json
import flask
from methods import internal_methods


@internal_methods.verifyServerID
@internal_methods.verifyDockerEngine(swarm_method=False)
def soloGetAppNames(server_id) -> flask.Response:
  """
  Returns an array of all apps, running or not

  parameters:
    server_id - this value is passed in the API route, for demo purposes this should always be "demo"
  """

  # executing system command
  completedProcess = internal_methods.subprocessRun(f"docker ps -a --format \"{{{{.Names}}}}\"")
  if completedProcess.returncode != 0:
    return flask.make_response("Unknown error:\n"+completedProcess.stdout.decode()+"\n"+completedProcess.stderr.decode(), 500)

  arr = []
  for string in completedProcess.stdout.decode().split("\n"):
    if string != "":
      arr.append(string)
  
  user = flask.request.args.get('user')
  if user != None:
    arr = [app for app in arr if app.split("--")[1] == user]

  return flask.make_response(json.dumps(arr), 200)