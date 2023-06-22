import subprocess
from flask import Response, request
from . import internal_methods


@internal_methods.verifyFacilityID
@internal_methods.verifyDockerEngine
def createApp(facility_id) -> Response:
  """

  """

  image_name = request.args.get("image")
  if image_name == None:
    return Response("No image name provided", status=400)

  version = request.args.get("version")
  if version == None:
    version = "latest"

  # checking if image exists
  completedProcess = subprocess.run(f"docker image ls --format \"{{{{.Repository}}}}\"", capture_output=True)
  if image_name not in completedProcess.stdout.decode().split("\n"):
    return Response(f"Could not find image \"{image_name}\"", status=400)

  # checking if container already exists
  completedProcess = subprocess.run(f"docker ps -a --format \"{{{{.Names}}}}\"", capture_output=True)
  print(completedProcess.stdout.decode().split("\n"))
  if image_name in completedProcess.stdout.decode().split("\n"):
    return Response("App already exists", status=400)

  # executing system command
  completedProcess = subprocess.run(f"docker create --name \"{image_name}\" --pull never {image_name}", capture_output=True)
  if completedProcess.returncode != 0:
    # uncaught error
    return Response(f"Failed to create app", status=500)

  return Response("Success", status=200)