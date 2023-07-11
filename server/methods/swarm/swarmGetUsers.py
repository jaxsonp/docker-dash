import flask
import json
from methods import internal_methods

@internal_methods.verifyServerID
@internal_methods.verifyDockerEngine(swarm_method=True)
def swarmGetUsers(server_id) -> flask.Response:
  """
  Returns an array of all users of existing containers

  parameters:
    server_id - this value is passed in the API route, for demo purposes this should always be "demo"
  """

  # get all services
  completedProcess = internal_methods.subprocessRun(f"docker service ls --format \"{{{{.Name}}}}\"")
  if completedProcess.returncode != 0:
    # uncaught error
    return flask.make_response("Uncaught error:\n"+completedProcess.stdout.decode()+"\n"+completedProcess.stderr.decode(), 500)

  # get user of each service
  arr = [s.split("--")[1] for s in completedProcess.stdout.decode().split("\n") if s != ""]

  return flask.make_response(json.dumps(list(set(arr))), 200)
