import os
import json
import time
import logging
import subprocess
from datetime import datetime, timedelta
from flask import request


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
    for container in _getContainers():
      logger = logging.getLogger(container)
      logger.setLevel(logging.INFO)

      # file logging
      fileHandler = logging.FileHandler(f"{dir_path}/logs/{container}.log", mode='a')
      fileHandler.setFormatter(formatter)
      logger.addHandler(fileHandler)

      completedProcess = subprocess.run("docker ps -a -f name={container} --format json", shell=True, capture_output=True)
      info = json.loads(completedProcess.stdout.decode().split("\n")[0])
      logger.info(f"{info['State']} [{info['Status']}]")

      logger.removeHandler(fileHandler)

    time.sleep(600)


def _getContainers() -> list:
  completedResponse = subprocess.run(f"docker ps -a --format \"{{{{.Names}}}}\"", shell=True, capture_output=True)
  return [s for s in completedResponse.stdout.decode().split("\n") if s]


if __name__ == "__main__":
  #print(getDailySummary("jupyter-lab"))
  loggingThreadFunc()