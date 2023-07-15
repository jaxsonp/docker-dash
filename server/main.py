from colorama import Fore, Style
import flask
from methods import internal_methods
import os
import sys
import threading

import logger

swarm_mode=False

app = flask.Flask(__name__)


@app.route('/')
def helper() -> flask.Response:
  with open("root_page.txt", "r") as f:
    return flask.Response(f.read(), mimetype='text/plain')




# SOLO ONLY METHODS ============================================================

from methods.solo.soloStartApp import soloStartApp
@app.route('/<server_id>/start-app', methods=['POST'])
def startAppWrapper(server_id) -> flask.Response:
  if swarm_mode:
    return flask.make_response("start-app endpoint incompatible with swarm mode", 400)
  else:
    return soloStartApp(server_id)


from methods.solo.soloStopApp import soloStopApp
@app.route('/<server_id>/stop-app', methods=['POST'])
def stopAppWrapper(server_id) -> flask.Response:
  if swarm_mode:
    return flask.make_response("stop-app endpoint incompatible with swarm mode", 400)
  else:
    return soloStopApp(server_id)


from methods.solo.soloPauseApp import soloPauseApp
@app.route('/<server_id>/pause-app', methods=['POST'])
def pauseAppWrapper(server_id) -> flask.Response:
  if swarm_mode:
    return flask.make_response("pause-app endpoint incompatible with swarm mode", 400)
  else:
    return soloPauseApp(server_id)


from methods.solo.soloUnpauseApp import soloUnpauseApp
@app.route('/<server_id>/unpause-app', methods=['POST'])
def unpauseAppWrapper(server_id) -> flask.Response:
  if swarm_mode:
    return flask.make_response("unpause-app endpoint incompatible with swarm mode", 400)
  else:
    return soloUnpauseApp(server_id)


from methods.solo.soloRestartApp import soloRestartApp
@app.route('/<server_id>/restart-app', methods=['POST'])
def restartAppWrapper(server_id) -> flask.Response:
  if swarm_mode:
    return flask.make_response("restart-app endpoint incompatible with swarm mode", 400)
  else:
    return soloRestartApp(server_id)


from methods.solo.soloDeleteApp import soloDeleteApp
@app.route('/<server_id>/delete-app', methods=['POST'])
def deleteAppWrapper(server_id) -> flask.Response:
  if swarm_mode:
    return flask.make_response("delete-app endpoint incompatible with swarm mode", 400)
  else:
    return soloDeleteApp(server_id)


from methods.solo.soloHardResetApp import soloHardResetApp
@app.route('/<server_id>/hard-reset-app', methods=['POST'])
def hardResetAppWrapper(server_id) -> flask.Response:
  if swarm_mode:
    return flask.make_response("hard-reset-app endpoint incompatible with swarm mode", 400)
  else:
    return soloHardResetApp(server_id)




# SWARM ONLY METHODS ===========================================================


from methods.swarm.swarmGetNodeInfo import swarmGetNodeInfo
@app.route('/<server_id>/get-node-info', methods=['GET'])
def getNodeInfoWrapper(server_id) -> flask.Response:
  if swarm_mode:
    return swarmGetNodeInfo(server_id)
  else:
    return flask.make_response("get-node-info endpoint incompatible with solo mode", 400)




# SOLO AND SWARM METHODS =======================================================


from methods.solo.soloKillApp import soloKillApp
from methods.swarm.swarmKillApp import swarmKillApp
@app.route('/<server_id>/kill-app', methods=['POST'])
def killAppWrapper(server_id) -> flask.Response:
  if swarm_mode:
    return swarmKillApp(server_id)
  else:
    return soloKillApp(server_id)


from methods.solo.soloCreateApp import soloCreateApp
from methods.swarm.swarmCreateApp import swarmCreateApp
@app.route('/<server_id>/create-app', methods=['POST'])
def createAppWrapper(server_id) -> flask.Response:
  if swarm_mode:
    return swarmCreateApp(server_id)
  else:
    return soloCreateApp(server_id)


from methods.solo.soloGetUsers import soloGetUsers
from methods.swarm.swarmGetUsers import swarmGetUsers
@app.route('/<server_id>/get-users', methods=['GET'])
def getUsersWrapper(server_id) -> flask.Response:
  if swarm_mode:
    return swarmGetUsers(server_id)
  else:
    return soloGetUsers(server_id)

from methods.solo.soloGetAppNames import soloGetAppNames
from methods.swarm.swarmGetAppNames import swarmGetAppNames
@app.route('/<server_id>/get-app-names', methods=['GET'])
def getAppNamesWrapper(server_id) -> flask.Response:
  if swarm_mode:
    return swarmGetAppNames(server_id)
  else:
    return soloGetAppNames(server_id)


from methods.solo.soloGetAppStatus import soloGetAppStatus
from methods.swarm.swarmGetAppStatus import swarmGetAppStatus
@app.route('/<server_id>/get-app-status', methods=['GET'])
def getAppStatusWrapper(server_id) -> flask.Response:
  if swarm_mode:
    return swarmGetAppStatus(server_id)
  else:
    return soloGetAppStatus(server_id)


from methods.solo.soloGetAppStats import soloGetAppStats
from methods.swarm.swarmGetAppStats import swarmGetAppStats
@app.route('/<server_id>/get-app-stats', methods=['GET'])
def getAppStatsWrapper(server_id) -> flask.Response:
  if swarm_mode:
    return swarmGetAppStats(server_id)
  else:
    return soloGetAppStats(server_id)


from methods.solo.soloGetAppInfo import soloGetAppInfo
from methods.swarm.swarmGetAppInfo import swarmGetAppInfo
@app.route('/<server_id>/get-app-info', methods=['GET'])
def getAppInfoWrapper(server_id) -> flask.Response:
  if swarm_mode:
    return swarmGetAppInfo(server_id)
  else:
    return soloGetAppInfo(server_id)
  

from methods.solo.soloGetNodeNames import soloGetNodeNames
from methods.swarm.swarmGetNodeNames import swarmGetNodeNames
@app.route('/<server_id>/get-node-names', methods=['GET'])
def getNodeNamesWrapper(server_id) -> flask.Response:
  if swarm_mode:
    return swarmGetNodeNames(server_id)
  else:
    return soloGetNodeNames(server_id)


from methods.solo.soloGetNodeStatus import soloGetNodeStatus
from methods.swarm.swarmGetNodeStatus import swarmGetNodeStatus
@app.route('/<server_id>/get-node-status', methods=['GET'])
def getNodeStatusWrapper(server_id) -> flask.Response:
  if swarm_mode:
    return swarmGetNodeStatus(server_id)
  else:
    return soloGetNodeStatus(server_id)



# AGNOSTIC METHODS =============================================================


from methods.agnostic.getUptimeSummary import getUptimeSummary
@app.route('/<server_id>/get-uptime-summary', methods=['GET'])
def getUptimeSummaryWrapper(server_id) -> flask.Response:
  return getUptimeSummary(server_id)


from methods.agnostic.requestImage import requestImage
@app.route('/<server_id>/request-image', methods=['POST'])
def requestImageWrapper(server_id) -> flask.Response:
  return requestImage(server_id)


from methods.agnostic.getImages import getImages
@app.route('/<server_id>/get-images', methods=['GET'])
def getImagesWrapper(server_id) -> flask.Response:
  return getImages(server_id)



def main(port=5000) -> None:
  print("\n\n\n")

  print(f" * Exporting PID: {os.getpid()}")
  pid_file_path = os.path.dirname(os.path.abspath(__file__))
  with open(f"{pid_file_path}/docker-dash.pid", "w") as pid_file:
    pid_file.write(str(os.getpid()))

  print(" * Checking swarm mode: ", end="")
  swarm_mode = internal_methods.checkSwarmMode()
  print(swarm_mode)

  print(" * Starting logging thread")
  logThread = threading.Thread(target=logger.loggingThreadFunc, daemon=True)
  logThread.start()

  completedProcess = internal_methods.subprocessRun("docker ps")
  if completedProcess.returncode != 0:
    print(Style.BRIGHT + Fore.RED + "WARNING: Docker does not appear to be running " + Style.RESET_ALL)

  app.run(port=port)



if __name__ == '__main__':
  port = 5000 # default port
  # getting port argument
  for i in range(len(sys.argv)):
    if (sys.argv[i] == "-p" or sys.argv[i] == "-port") and i + 1 < len(sys.argv):
      try:
        port = int(sys.argv[i + 1])
      except ValueError:
        pass
      finally:
        break

  main(port)