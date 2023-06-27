import subprocess
import json
import flask
from . import internal_methods


@internal_methods.verifyFacilityID
@internal_methods.verifyDockerEngine
def getImages(facility_id) -> flask.Response:
  """
  Returns an array of all local images

  parameters:
    facility_id - this value is passed in the API route, for demo purposes this should always be "demo"
  """

  # executing system command
  completedProcess = internal_methods.subprocessRun(f"docker images --format json", shell=True, capture_output=True)
  if completedProcess.returncode != 0:
    return flask.make_response("Unknown error:\n"+completedProcess.stdout.decode()+"\n"+completedProcess.stderr.decode(), 500)

  output_list = completedProcess.stdout.decode().strip().split("\n")
  print(output_list)
  output_list = [json.dumps(json.loads(s)) if s != '' else s for s in output_list]

  return flask.make_response(f"[{', '.join(output_list)}]", 200)