import os
import json
import time
import logging
import subprocess
from datetime import datetime, timedelta


container_state_codes = {
  "created": 0,
  "running": 1,
  "restarting": 2,
  "exited": 3,
  "paused": 4,
  "dead": 5
}
format_str = '%Y-%m-%dT%H:%M:%S'
dir_path = os.path.dirname(os.path.realpath(__file__))
formatter = logging.Formatter('%(asctime)s: %(message)s', datefmt=format_str)

def loggingThreadFunc() -> None:

  # make log dir if it doesnt exist
  if not os.path.exists(f'{dir_path}/logs'):
    os.makedirs(f'{dir_path}/logs')

  while True:
    containers = _getContainers()
    for container in containers:
      logger = logging.getLogger(container)
      logger.setLevel(logging.INFO)

      # file logging
      fileHandler = logging.FileHandler(f"{dir_path}/logs/{container}.log", mode='a')
      fileHandler.setFormatter(formatter)
      logger.addHandler(fileHandler)

      completedProcess = subprocess.run(f"docker ps -a -f name={container} --format json", capture_output=True)
      info = json.loads(completedProcess.stdout.decode().split("\n")[0])
      logger.info(f"{info['State']} [{info['Status']}]")

      logger.removeHandler(fileHandler)

    time.sleep(600)


def get24hrSummary(name: str) -> list | None:
  if os.path.isfile(f"{dir_path}/logs/{name}.log"):
    output = {}
    with open(f"{dir_path}/logs/{name}.log", "r") as log:
      for line in log.readlines():
        timestamp = datetime.strptime(line.split(": ")[0], format_str)
        state = line.split(" ")[1]
        if timestamp + timedelta(days=1) > datetime.now():
          output.update({timestamp.isoformat(): container_state_codes[state]})
    return output
  return None
  #datetime.strptime(date_string, format)


def _getContainers() -> list:
  completedResponse = subprocess.run(f"docker ps -a --format \"{{{{.Names}}}}\"", capture_output=True)
  arr = []
  for string in completedResponse.stdout.decode().split("\n"):
    if string != "":
      arr.append(string)
  return arr


if __name__ == "__main__":
  #print(getDailySummary("jupyter-lab"))
  loggingThreadFunc()