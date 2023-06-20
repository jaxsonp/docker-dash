import os
import json
import time
import logging
import subprocess

"""
1 - Created
2 - Running
3 - Restarting
4 - Exited
5 - Paused
6 - Dead
"""

dir_path = os.path.dirname(os.path.realpath(__file__))
formatter = logging.Formatter('%(asctime)s: %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

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


def getDailySummary():

  return


def _getContainers() -> list:
  completedResponse = subprocess.run(f"docker ps -a --format \"{{{{.Names}}}}\"", capture_output=True)
  arr = []
  for string in completedResponse.stdout.decode().split("\n"):
    if string != "":
      arr.append(string)
  return arr


if __name__ == "__main__":
  loggingThreadFunc()