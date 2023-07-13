import flask
from methods import internal_methods

@internal_methods.verifyServerID
@internal_methods.verifyDockerEngine(swarm_method=False)
def soloCreateApp(server_id) -> flask.Response:
  """
  Creates an app container from a given image and user

  parameters:
    server_id - this value is passed in the API route, for demo purposes this should always be "demo"
    image - this value is passed as an http parameter
    user - this value is passed as an http parameter
    version (optional) - this value is passed as an http parameter
  """

  image_name = flask.request.args.get("image")
  if image_name == None:
    return flask.Response("No image name provided", status=400)
  image_name = image_name.split(":")[0]

  user_name = flask.request.args.get("user")
  if user_name == None:
    return flask.Response("No user name provided", status=400)

  version = flask.request.args.get("version")
  if version == None:
    version = "latest"

  # checking if image exists
  completedProcess = internal_methods.subprocessRun(f"docker image ls --format \"{{{{.Repository}}}}\"")
  if image_name not in completedProcess.stdout.decode().split("\n"):
    return flask.Response(f"Could not find image \"{image_name}\"", status=400)

  container_name = image_name + "--" + user_name

  # checking if container already exists
  completedProcess = internal_methods.subprocessRun(f"docker ps -a --format \"{{{{.Names}}}}\"")
  if container_name in completedProcess.stdout.decode().split("\n"):
    return flask.Response("App already exists", status=400)

  # create container
  completedProcess = internal_methods.subprocessRun(f"docker create --name \"{container_name}\" --pull never {image_name}")
  if completedProcess.returncode != 0:
    # uncaught error
    return flask.make_response("Failed to create app:\n"+completedProcess.stdout.decode()+"\n"+completedProcess.stderr.decode(), 500)

  return flask.make_response("Success", 200)