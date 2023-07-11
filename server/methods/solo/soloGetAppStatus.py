import flask
import json
from methods import internal_methods

@internal_methods.verifyServerID
@internal_methods.verifyDockerEngine(swarm_method=False)
def soloGetAppStatus(server_id) -> flask.Response:
  """
  Returns basic information and status of the specified app, or all apps if no name is provided.

  parameters:
    server_id - this value is passed in the API route, for demo purposes this should always be "demo"
    app_name (optional) - this value is passed as an http parameter

  returns:
    if successful, returns app information in json format
  """

  app_name = flask.request.args.get("name")
  if app_name == None:

    # executing docker command
    completedProcess = internal_methods.subprocessRun(f"docker ps -a --format json")
    if completedProcess.returncode != 0:
      # uncaught error
      return flask.make_response(f"Uncaught error\n"+completedProcess.stdout.decode()+"\n"+completedProcess.stderr.decode(), 500)

    # process output
    output_list = completedProcess.stdout.decode().strip().split("\n")
    output_list = [json.dumps(json.loads(s)) for s in output_list]
    
    return flask.make_response(f"[{', '.join(output_list)}]", 200)
    
  else:

    # verify name
    app_id = internal_methods.getContainerID(app_name)
    if app_id == None:
      return flask.make_response(f"Unable to find app \"{app_name}\"", 400)

    # executing system command
    completedProcess = internal_methods.subprocessRun(f"docker ps -a -f id={app_id} --format json")
    if completedProcess.returncode != 0:
      return flask.make_response(f"Failed to query app:\n"+completedProcess.stdout.decode()+"\n"+completedProcess.stderr.decode(), 500)

    output_list = completedProcess.stdout.decode().split("\n")
    output_list = map(json.loads, output_list)

    # docker ps returns a list of containers with matching names, so we must search for the one that matches exactly
    for entry in output_list:
      if entry["Names"] == app_name:
        return flask.make_response(json.dumps(entry), 200)

    return flask.make_response("Something went wrong with soloGetAppStatus", 500)