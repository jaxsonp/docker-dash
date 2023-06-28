import json
import flask
from . import internal_methods

@internal_methods.verifyFacilityID
@internal_methods.verifyDockerEngine(swarm_method=True)
def swarmGetAppStats(facility_id, app_name="", app_id="") -> flask.Response:
  """
  Returns computing stats of the specified app, or all apps if no name is provided.

  parameters:
    facility_id (optional) - this value is passed in the API route, for demo purposes this should always be "demo"
    app_name - this value is passed as an http parameter

  returns:
    if successful, returns app information in json format
  """

  # executing system command
  completedProcess = internal_methods.subprocessRun(f"docker stats -a --no-stream --format json", shell=True, capture_output=True)
  if completedProcess.returncode != 0:
      return flask.make_response(f"Failed to query app:\n"+completedProcess.stdout.decode()+"\n"+completedProcess.stderr.decode(), 500)

  output_list = completedProcess.stdout.decode().strip().split("\n")

  app_name = flask.request.args.get("name")
  if app_name == None:

    output_list = [json.dumps(json.loads(s)) for s in output_list]
    return flask.make_response(f"[{', '.join(output_list)}]", 200)
    
  else:

    output_list = map(json.loads, output_list)

    #find entry with matching name
    for entry in output_list:
      name_list = entry["Name"].split(".")
      if len(name_list) < 3: continue
      if name_list[0] == app_name:
        return flask.make_response(json.dumps(entry), 200)

    return flask.make_response(f"Unable to find app \"{app_name}\"", 400)