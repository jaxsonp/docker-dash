from flask import Flask, request, Response
import subprocess
import json

app = Flask(__name__)


@app.route('/<dsrc>/queryStatus')
def statusQuery(dsrc):
  """

  """
  container_name = request.args.get("container")

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

  return Response("", status=500)


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