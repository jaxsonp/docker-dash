from datetime import datetime, timedelta
import flask
import json
import logger
from methods import internal_methods
import os


@internal_methods.verifyServerID
@internal_methods.handleAppName
def getUptimeSummary(server_id, app_name="", app_id="") -> flask.Response:
  """
  Returns a summary of the health/uptime of an app

  parameters:
    server_id - this value is passed in the API route, for demo purposes this should always be "demo"
    app_name - this value is passed as an http parameter
    app_id - this value is obtained when the app_name is verified with the handleAppName decorator
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
  if not os.path.isfile(f"{logger.dir_path}/logs/{app_name}.log"):
    return flask.make_response(f"Could not find log for \"{app_name}\"", 400)
  
  # check if in swarm mode
  swarmMode = internal_methods.checkSwarmMode()
  
  output = {}
  def updateOutput():
    if swarmMode: output.update({timestamp.isoformat(): "running" in state.lower()})
    else:         output.update({timestamp.isoformat(): state == "running"})

  # read log file
  with open(f"{logger.dir_path}/logs/{app_name}.log", "r") as log:
    for line in log.readlines():
      timestamp = datetime.strptime(line.split(": ")[0], logger.date_format_str)
      state = line.split(" ")[1]

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
