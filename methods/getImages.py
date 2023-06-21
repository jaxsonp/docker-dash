import subprocess
import json
from flask import Response
from . import internal_methods


@internal_methods.verifyFacilityID
@internal_methods.verifyDockerEngine
def getImages(facility_id) -> Response:
  """
  Returns an array of all local images

  parameters:
    facility_id - this value is passed in the API route, for demo purposes this should always be "demo"
  """

  # executing system command
  completedResponse = subprocess.run(f"docker images --format json", capture_output=True)
  if completedResponse.returncode != 0:
    return Response("Unknown error", status=500)

  output_list = completedResponse.stdout.decode().strip().split("\n")
  output_list = [json.dumps(json.loads(s)) for s in output_list]
  output_str = f"[{', '.join(output_list)}]"
  
  print(output_str)

  return Response(output_str, 200)