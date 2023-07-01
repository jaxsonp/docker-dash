import os
import json
import time
import logging
from methods import internal_methods
from flask import request


container_state_codes = {
  "created": 0,
  "running": 1,
  "restarting": 2,
  "exited": 3,
  "paused": 4,
  "dead": 5
}
date_format_str = '%Y-%m-%dT%H:%M:%S'
dir_path = os.path.dirname(os.path.realpath(__file__))
formatter = logging.Formatter('%(asctime)s: %(message)s', datefmt=date_format_str)

def loggingThreadFunc() -> None:

  # make log dir if it doesnt exist
  if not os.path.exists(f'{dir_path}/logs'):
    os.makedirs(f'{dir_path}/logs')

  while True:
    for container in _getContainers():

      # checking if its in swarm mode
      log_str = ""
      completedProcess = internal_methods.subprocessRun("docker info --format json")
      if json.loads(completedProcess.stdout.decode())["Swarm"]["LocalNodeState"] == "active":
        # swarm mode
        completedProcess = internal_methods.subprocessRun(f"docker service ps -f desired-state=complete --format json {container}")
        info = json.loads(completedProcess.stdout.decode().split("\n")[0])
        if info == {}:
          continue
        log_str = info['CurrentState']
      else:
        # solo mode
        completedProcess = internal_methods.subprocessRun(f"docker ps -a -f name={container} --format json")
        info = json.loads(completedProcess.stdout.decode().split("\n")[0])
        if info == {}:
          continue
        log_str = f"{info['State']} [{info['Status']}]"

      # logging file setup
      logger = logging.getLogger(container)
      logger.setLevel(logging.INFO)

      fileHandler = logging.FileHandler(f"{dir_path}/logs/{container}.log", mode='a')
      fileHandler.setFormatter(formatter)
      logger.addHandler(fileHandler)
      logger.info(log_str)

      logger.removeHandler(fileHandler)

    time.sleep(600)


def _getContainers() -> list:

  # checking if its in swarm mode
  completedProcess = internal_methods.subprocessRun("docker info --format json")
  if json.loads(completedProcess.stdout.decode())["Swarm"]["LocalNodeState"] == "active":
    completedProcess = internal_methods.subprocessRun(f"docker service ls --format \"{{{{.Name}}}}\"")
  else:
    completedProcess = internal_methods.subprocessRun(f"docker ps -a --format \"{{{{.Names}}}}\"")
  return [s for s in completedProcess.stdout.decode().split("\n") if s]


if __name__ == "__main__":
  #print(getDailySummary("jupyter-lab"))
  loggingThreadFunc()