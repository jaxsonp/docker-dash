import flask
import json
from methods import internal_methods

@internal_methods.verifyServerID
@internal_methods.verifyDockerEngine(swarm_method=False)
def soloGetAppStats(server_id) -> flask.Response:
  """
  Returns hardware and resource stats of the specified app, or all apps if no name is provided.

  parameters:
    server_id - this value is passed in the API route, for demo purposes this should always be "demo"
    app_name (optional) - this value is passed as an http parameter

  returns:
    if successful, returns app stats in json format
  """

  # executing docker command
  completedProcess = internal_methods.subprocessRun(f"docker stats -a --no-stream --format json")
  if completedProcess.returncode != 0:
    # uncaught error
    return flask.make_response(f"Uncaught error:\n"+completedProcess.stdout.decode()+"\n"+completedProcess.stderr.decode(), 500)

  output_list = completedProcess.stdout.decode().strip().split("\n")

  app_name = flask.request.args.get("name")
  if app_name == None:

    # return all
    output_list = [json.dumps(json.loads(s)) for s in output_list]
    return flask.make_response(f"[{', '.join(output_list)}]", 200)
    
  else:

    # verify name
    app_id = internal_methods.getContainerID(app_name)
    if app_id == None:
      return flask.make_response(f"Unable to find app \"{app_name}\"", 400)

    output_list = map(json.loads, output_list)

    #find entry with matching name
    for entry in output_list:
      if entry["ID"] == app_id:
        return flask.make_response(json.dumps(entry), 200)

    return flask.make_response("This should not be reached", 500)