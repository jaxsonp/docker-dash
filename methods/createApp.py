import subprocess
from flask import Response, request
from . import internal_methods


@internal_methods.verifyFacilityID
@internal_methods.verifyDockerEngine
def createApp(facility_id) -> Response:
  """

  """

  image_name = request.args.get("name")
  if image_name == None:
    return Response("No container name provided", status=400)

  # checking if image exists
  completedProcess = subprocess.run(f"docker image ls \"{{.Repository}}\"", capture_output=True)
  if image_name not in completedProcess.stdout.decode().split("\n"):
    return Response("No container name provided", status=400)

  # executing system command
  completedProcess = subprocess.run(f"docker create --pull never {image_name}", capture_output=True)
  if completedProcess.returncode != 0:
    # uncaught error
    return Response(f"Failed to create app", status=500)

  return Response(status=500)