import subprocess
from flask import Response, request
from . import internal_methods


@internal_methods.verifyFacilityID
@internal_methods.verifyDockerEngine
def requestImage(facility_id) -> Response:
  """
  Request an image to be pulled from docker hub

  parameters:
    facility_id - this value is passed in the API route, for demo purposes this should always be "demo"
    image_name - this value is passed as an http parameter
  """

  image_name = request.args.get("image")
  if image_name == None:
    return Response("No image name provided", status=400)

  # *insert security verification here*

  # try to pull app from docker hub
  completedResponse = subprocess.run(f"docker pull {image_name}", capture_output=True)
  if completedResponse.returncode != 0:
    return Response(f"Could not pull image '{image_name}'", status=400)
  return Response("Success", status=200)