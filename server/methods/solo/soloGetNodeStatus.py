import flask
import json
from methods import internal_methods

@internal_methods.verifyServerID
def soloGetNodeStatus(server_id) -> flask.Response:
  """
  Returns status of the local machine

  parameters:
    server_id - this value is passed in the API route, for demo purposes this should always be "demo"

  returns:
    if successful, returns node status in json format
  """

  # get local hostname
  completedProcess = internal_methods.subprocessRun("hostname")
  local_hostname = completedProcess.stdout.decode().strip()

  # check that docker is running
  status = "Ready"
  completedProcess = internal_methods.subprocessRun("docker ps")
  if completedProcess.returncode != 0:
    status = "Down"

  resp = [{"Availability":"Active", "Hostname":local_hostname, "ManagerStatus":"Leader", "Self":True, "Status":status}]

  return flask.make_response(json.dumps(resp), 200)