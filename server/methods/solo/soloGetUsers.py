import flask
import json
from methods import internal_methods

@internal_methods.verifyServerID
@internal_methods.verifyDockerEngine(swarm_method=False)
def soloGetUsers(server_id) -> flask.Response:
  """
  Returns an array of all users of existing containers

  parameters:
    server_id - this value is passed in the API route, for demo purposes this should always be "demo"
  """

  # get all containers
  completedProcess = internal_methods.subprocessRun(f"docker ps -a --format \"{{{{.Names}}}}\"")
  if completedProcess.returncode != 0:
    # uncaught error
    return flask.make_response("Uncaught error:\n"+completedProcess.stdout.decode()+"\n"+completedProcess.stderr.decode(), 500)

  # get user of each container
  arr = []
  for string in completedProcess.stdout.decode().split("\n"):
    if string != "":
      arr.append(string.split("--")[1])

  return flask.make_response(json.dumps(list(set(arr))), 200)