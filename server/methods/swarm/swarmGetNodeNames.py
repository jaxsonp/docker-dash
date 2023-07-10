import json
import flask
from methods import internal_methods

@internal_methods.verifyServerID
@internal_methods.verifyDockerEngine(swarm_method=True)
def swarmGetNodeNames(server_id, app_name="", app_id="") -> flask.Response:
  """
  Returns a list of all nodes in the swarm

  parameters:
    server_id - this value is passed in the API route, for demo purposes this should always be "demo"

  returns:
    if successful, returns node names in json format
  """

  completedProcess = internal_methods.subprocessRun("docker node ls --format {{.Hostname}}")
  if completedProcess.returncode != 0:
      return flask.make_response(f"Unknown error:\n"+completedProcess.stdout.decode()+"\n"+completedProcess.stderr.decode(), 500)

  arr = [s for s in completedProcess.stdout.decode().split("\n") if s != ""]

  return flask.make_response(json.dumps(arr), 200)