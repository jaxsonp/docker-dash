import subprocess
import json
from flask import Response, request
from . import internal_methods

@internal_methods.verifyFacilityID
@internal_methods.verifyDockerEngine
def getAppStats(facility_id, app_name="", app_id="") -> Response:
  """
  Returns computing stats of the specified app, or all apps if no name is provided.

  parameters:
    facility_id (optional) - this value is passed in the API route, for demo purposes this should always be "demo"
    app_name - this value is passed as an http parameter

  returns:
    if successful, returns app information in json format
  """

  app_name = request.args.get("name")

  # executing system command
  completedProcess = subprocess.run(f"docker stats -a --no-stream --format json", capture_output=True)
  if completedProcess.returncode != 0:
      return Response(f"Failed to query app", status=500)

  output_list = completedProcess.stdout.decode().strip().split("\n")

  if app_name == None:

    output_list = [json.dumps(json.loads(s)) for s in output_list]
    return Response(f"[{', '.join(output_list)}]", status=200)
    
  else:

    # verify name
    app_id = internal_methods.getContainerID(app_name)
    if app_id == None:
      return Response(f"Unable to find app \"{app_name}\"", status=400)

    output_list = map(json.loads, output_list)

    #find entry with matching name
    for entry in output_list:
      if entry["ID"] == app_id:
        return Response(json.dumps(entry), status=200)

    return Response("This should not be reached", status=500)