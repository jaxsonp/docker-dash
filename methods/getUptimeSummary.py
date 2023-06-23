import os
import json
from datetime import datetime, timedelta
from flask import Response, request


from . import internal_methods
import logger


@internal_methods.verifyFacilityID
@internal_methods.verifyDockerEngine
@internal_methods.handleAppName
def getUptimeSummary(facility_id, app_name="", app_id="") -> Response:
  """
  Returns a summary of the health/uptime of an app

  parameters:
    facility_id - this value is passed in the API route, for demo purposes this should always be "demo"
    app_name - this value is passed as an http parameter
    duration - this value is passed as an http parameter to specify duration of
      log data to return. (hour, day, week, or month)

  returns:
    returns a timestamped list of bools representing uptime
  """

  # validating duration
  duration = request.args.get("duration")
  if duration == None:
    return Response("No duration provided", status=400)

  if duration not in ["hour", "day", "week", "month"]:
    return Response("Invalid duration", status=400)

  # checking if log exists
  if os.path.isfile(f"{logger.dir_path}/logs/{app_name}.log"):
    output = {}

    with open(f"{logger.dir_path}/logs/{app_name}.log", "r") as log:
      for line in log.readlines():
        timestamp = datetime.strptime(line.split(": ")[0], logger.format_str)
        state = line.split(" ")[1]

        if duration == "hour":
          if timestamp + timedelta(hours=1) > datetime.now():
            output.update({timestamp.isoformat(): state == "running"})
        elif duration == "day":
          if timestamp + timedelta(days=1) > datetime.now():
            output.update({timestamp.isoformat(): state == "running"})
        elif duration == "week":
          if timestamp + timedelta(days=7) > datetime.now():
            output.update({timestamp.isoformat(): state == "running"})
        elif duration == "month":
          if timestamp + timedelta(days=30) > datetime.now():
            output.update({timestamp.isoformat(): state == "running"})

    return Response(json.dumps(output), 200)

  return Response(f"Could not find log for \"{app_name}\"", status=400)