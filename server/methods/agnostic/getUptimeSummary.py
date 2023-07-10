import os
import json
from datetime import datetime, timedelta
import flask


from methods import internal_methods
import logger


@internal_methods.verifyServerID
@internal_methods.handleAppName
def getUptimeSummary(server_id, app_name="", app_id="") -> flask.Response:
  """
  Returns a summary of the health/uptime of an app

  parameters:
    server_id - this value is passed in the API route, for demo purposes this should always be "demo"
    app_name - this value is passed as an http parameter
    duration - this value is passed as an http parameter to specify duration of
      log data to return. (hour, day, week, or month)

  returns:
    returns a timestamped list of bools representing uptime
  """

  # validating duration
  duration = flask.request.args.get("duration")
  if duration == None:
    return flask.make_response("No duration provided", 400)

  if duration not in ["hour", "day", "week", "month"]:
    return flask.make_response("Invalid duration", 400)

  # checking if log exists
  if os.path.isfile(f"{logger.dir_path}/logs/{app_name}.log"):
    output = {}

    with open(f"{logger.dir_path}/logs/{app_name}.log", "r") as log:
      for line in log.readlines():
        timestamp = datetime.strptime(line.split(": ")[0], logger.date_format_str)
        state = line.split(" ")[1]
        
        def updateOutput():
          completedProcess = internal_methods.subprocessRun("docker info --format json")
          if json.loads(completedProcess.stdout.decode())["Swarm"]["LocalNodeState"] == "active":
            output.update({timestamp.isoformat(): "running" in state.lower()})
          else:
            output.update({timestamp.isoformat(): state == "running"})

        if duration == "hour":
          if timestamp + timedelta(hours=1) > datetime.now():
            updateOutput()
        elif duration == "day":
          if timestamp + timedelta(days=1) > datetime.now():
            updateOutput()
        elif duration == "week":
          if timestamp + timedelta(days=7) > datetime.now():
            updateOutput()
        elif duration == "month":
          if timestamp + timedelta(days=30) > datetime.now():
            updateOutput()

    return flask.make_response(json.dumps(output), 200)

  return flask.make_response(f"Could not find log for \"{app_name}\"", 400)