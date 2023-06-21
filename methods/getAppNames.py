import subprocess
import json
from flask import Response
from . import internal_methods


@internal_methods.verifyFacilityID
@internal_methods.verifyDockerEngine
def getAppNames(facility_id) -> Response:
  """
  Returns an array of all apps, running or not

  parameters:
    facility_id - this value is passed in the API route, for demo purposes this should always be "demo"
  """

  # executing system command
  completedResponse = subprocess.run(f"docker ps -a --format \"{{{{.Names}}}}\"", capture_output=True)
  if completedResponse.returncode != 0:
    return Response("Unknown error", status=500)

  arr = []
  for string in completedResponse.stdout.decode().split("\n"):
    if string != "":
      arr.append(string)

  return Response(json.dumps(arr), 200)