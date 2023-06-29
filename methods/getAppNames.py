import subprocess
import json
import flask
from . import internal_methods


@internal_methods.verifyFacilityID
@internal_methods.verifyDockerEngine(swarm_method=False)
def getAppNames(facility_id) -> flask.Response:
  """
  Returns an array of all apps, running or not

  parameters:
    facility_id - this value is passed in the API route, for demo purposes this should always be "demo"
  """

  # executing system command
  completedProcess = internal_methods.subprocessRun(f"docker ps -a --format \"{{{{.Names}}}}\"")
  if completedProcess.returncode != 0:
    return flask.make_response("Unknown error:\n"+completedProcess.stdout.decode()+"\n"+completedProcess.stderr.decode(), 500)

  arr = []
  for string in completedProcess.stdout.decode().split("\n"):
    if string != "":
      arr.append(string)

  return flask.make_response(json.dumps(arr), 200)