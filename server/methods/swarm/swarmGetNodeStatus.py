import json
import flask
from methods import internal_methods

@internal_methods.verifyServerID
@internal_methods.verifyDockerEngine(swarm_method=True)
def swarmGetNodeStatus(server_id, app_name="", app_id="") -> flask.Response:
  """
  Returns status of specified node, or all nodes if not specified

  parameters:
    server_id - this value is passed in the API route, for demo purposes this should always be "demo"
    app_name (optional) - this value is passed as an http parameter

  returns:
    if successful, returns node status in json format
  """

  # get list of node names
  completedProcess = internal_methods.subprocessRun("docker node ls --format {{.Hostname}}")
  if completedProcess.returncode != 0:
      return flask.make_response(f"Unknown error:\n"+completedProcess.stdout.decode()+"\n"+completedProcess.stderr.decode(), 500)
  name_list = completedProcess.stdout.decode().strip().split("\n")

  hostname = flask.request.args.get("hostname")

  if hostname == None:

    # get all node statuses
    completedProcess = internal_methods.subprocessRun(f"docker node ls --format json")
    if completedProcess.returncode != 0:
      return flask.make_response(f"Failed to query apps\n"+completedProcess.stdout.decode()+"\n"+completedProcess.stderr.decode(), 500)

    output_list = completedProcess.stdout.decode().strip().split("\n")
    output_list = [json.dumps(json.loads(s)) for s in output_list]
    
    return flask.make_response(f"[{', '.join(output_list)}]", 200)
  
  else:

    # check that node exists
    if hostname not in name_list:
      return flask.make_response(f"Unable to find node '{hostname}'", 400)

    # get specified node status
    completedProcess = internal_methods.subprocessRun(f"docker node ls -f name={hostname} --format json")
    if completedProcess.returncode != 0:
      return flask.make_response(f"Unknown error:\n"+completedProcess.stdout.decode()+"\n"+completedProcess.stderr.decode(), 500)

    return flask.make_response(json.dumps(json.loads(completedProcess.stdout.decode())), 200)