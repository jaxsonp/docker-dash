import json
import flask
from . import internal_methods

@internal_methods.verifyFacilityID
@internal_methods.verifyDockerEngine(swarm_method=True)
def swarmGetNodeNames(facility_id, app_name="", app_id="") -> flask.Response:
  """
  Returns a list of all nodes in the swarm

  parameters:
    facility_id - this value is passed in the API route, for demo purposes this should always be "demo"

  returns:
    if successful, returns node names in json format
  """

  completedProcess = internal_methods.subprocessRun("docker node ls --format {{.Hostname}}", shell=True, capture_output=True)
  if completedProcess.returncode != 0:
      return flask.make_response(f"Unknown error:\n"+completedProcess.stdout.decode()+"\n"+completedProcess.stderr.decode(), 500)

  arr = [s for s in completedProcess.stdout.decode().split("\n") if s != ""]

  return flask.make_response(json.dumps(arr), 200)