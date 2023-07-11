from collections import Counter
import flask
import json
from methods import internal_methods


@internal_methods.verifyServerID
@internal_methods.verifyDockerEngine()
def getImages(server_id) -> flask.Response:
  """
  Returns an array of information on all installed images

  parameters:
    server_id - this value is passed in the API route, for demo purposes this should always be "demo"
  """

  # getting all containers
  completedProcess = None
  if internal_methods.checkSwarmMode():
    completedProcess = internal_methods.subprocessRun(f"docker service ls --format \"{{{{.Image}}}}\"")
  else:
    completedProcess = internal_methods.subprocessRun(f"docker ps -a --format \"{{{{.Image}}}}\"")
  imageCounter = Counter([s.split(":")[0] for s in completedProcess.stdout.decode().split("\n")])

  # getting all images
  completedProcess = internal_methods.subprocessRun(f"docker images --format json")
  if completedProcess.returncode != 0:
    return flask.make_response("Unknown error:\n"+completedProcess.stdout.decode()+"\n"+completedProcess.stderr.decode(), 500)

  # load json and add CreatedContainerCount
  output_list = []
  for image in completedProcess.stdout.decode().strip().split("\n"):
    if image == "": continue
    image_json = json.loads(image)
    image_json.update({"CreatedContainerCount": imageCounter[image_json["Repository"]]})
    output_list.append(json.dumps(image_json))

  return flask.make_response(f"[{', '.join(output_list)}]", 200)