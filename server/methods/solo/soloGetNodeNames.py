import flask
import json
from methods import internal_methods

@internal_methods.verifyServerID
@internal_methods.verifyDockerEngine(swarm_method=False)
def soloGetNodeNames(server_id) -> flask.Response:
  """
  Returns local hostname

  parameters:
    server_id - this value is passed in the API route, for demo purposes this should always be "demo"
  """

  completedProcess = internal_methods.subprocessRun("hostname")
  local_hostname = completedProcess.stdout.decode().strip()

  return flask.make_response(f"[{local_hostname}]", 200)