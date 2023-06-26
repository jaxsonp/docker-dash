import subprocess
import flask
from . import internal_methods


@internal_methods.verifyFacilityID
@internal_methods.verifyDockerEngine
def requestImage(facility_id) -> flask.Response:
  """
  Request an image to be pulled from docker hub

  parameters:
    facility_id - this value is passed in the API route, for demo purposes this should always be "demo"
    image_name - this value is passed as an http parameter
  """

  image_name = flask.request.args.get("image")
  if image_name == None:
    return flask.make_response("No image name provided", 400)

  # *insert security verification here*

  # try to pull app from docker hub
  completedProcess = subprocess.run(f"docker pull {image_name}", shell=True, capture_output=True)
  if completedProcess.returncode != 0:
    return flask.make_response(f"Could not pull image '{image_name}':\n"+completedProcess.stdout.decode()+"\n"+completedProcess.stderr.decode(), 400)
  return flask.make_response("Success", 200)