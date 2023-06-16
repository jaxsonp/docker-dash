from flask import Flask, request, Response
import subprocess
import json

app = Flask(__name__)


@app.route('/<dsrc>/queryStatus')
def statusQuery(dsrc):
  """
  Returns basic information and status of specified container.
  
  parameters:
    dsrc - this value is passed in the API route, for demo purposes this should always be mhpcc
    container_name - this value is passed as an http parameter

  returns:
    if successful, returns container information in json format
  """
  container_name = request.args.get("container")

  # this is temporary just for the demo
  if dsrc != "mhpcc":
    return Response("Unable to locate DSRC", status=404)

  # executing system command
  output_list = subprocess.check_output(f"docker ps -a -f name={container_name} --format json").decode().split("\n")
  output_list = map(json.loads, output_list)

  # docker ps returns a list of containers with matching ames, so we must search
  # for the one that matches exactly
  for entry in output_list:
    if entry["Names"] == container_name:
      return Response(json.dumps(entry), status=200)

  # container couldn't be found
  return Response(f"Unable to find app: {container_name}", status=500)


@app.route('/<dsrc>/inspectContainer')
def inspectContainer(dsrc):
  """

  """
  container_name = request.args.get("container")

  if dsrc != "mhpcc":
    return Response("Unable to locate DSRC", status=404)

  # executing system command
  output_list = json.loads(subprocess.check_output(f"docker inspect --type=container {container_name}").decode())

  # docker inspect returns a list of containers, so we must search for the one
  # with a matching container name
  for entry in output_list:
    if entry["Name"].replace("/", "") == container_name:
      return Response(json.dumps(entry), status=200)

  return Response("", status=500)


if __name__ == '__main__':
  print("\n\n\n")
  app.run()