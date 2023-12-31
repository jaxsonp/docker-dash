import flask
from methods import internal_methods


@internal_methods.verifyServerID
@internal_methods.verifyDockerEngine()
def requestImage(server_id) -> flask.Response:
  """
  Request an image to be pulled from docker hub

  parameters:
    server_id - this value is passed in the API route, for demo purposes this should always be "demo"
    image_name - this value is passed as an http parameter
  """

  # verify image name
  image_name = flask.request.args.get("image")
  if image_name == None:
    return flask.make_response("No image name provided", 400)

  """
  ===== insert security verification here =====
  """

  # try to pull app from docker hub
  completedProcess = internal_methods.subprocessRun(f"docker pull {image_name}")
  if completedProcess.returncode != 0:
    return flask.make_response(f"Could not pull image '{image_name}':\n"+completedProcess.stdout.decode()+"\n"+completedProcess.stderr.decode(), 400)
  return flask.make_response("Success", 200)