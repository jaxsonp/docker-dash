import sys
import flask
import threading
from colorama import Fore, Style
from methods import internal_methods

import logger

swarm_mode=False

app = flask.Flask(__name__)


@app.route('/')
def helper() -> flask.Response:
  with open("root_page.txt", "r") as f:
    return flask.Response(f.read(), mimetype='text/plain')


from methods.solo.soloStartApp import soloStartApp
@app.route('/<facility_id>/start-app', methods=['POST'])
def startAppWrapper(facility_id) -> flask.Response:
  if swarm_mode:
    return flask.make_response("start-app endpoint incompatible with swarm mode", 400)
  else:
    return soloStartApp(facility_id)


from methods.solo.soloStopApp import soloStopApp
@app.route('/<facility_id>/stop-app', methods=['POST'])
def stopAppWrapper(facility_id) -> flask.Response:
  if swarm_mode:
    return flask.make_response("stop-app endpoint incompatible with swarm mode", 400)
  else:
    return soloStopApp(facility_id)


from methods.solo.soloPauseApp import soloPauseApp
@app.route('/<facility_id>/pause-app', methods=['POST'])
def pauseAppWrapper(facility_id) -> flask.Response:
  if swarm_mode:
    return flask.make_response("pause-app endpoint incompatible with swarm mode", 400)
  else:
    return soloPauseApp(facility_id)


from methods.solo.soloUnpauseApp import soloUnpauseApp
@app.route('/<facility_id>/unpause-app', methods=['POST'])
def unpauseAppWrapper(facility_id) -> flask.Response:
  if swarm_mode:
    return flask.make_response("unpause-app endpoint incompatible with swarm mode", 400)
  else:
    return soloUnpauseApp(facility_id)


from methods.solo.soloRestartApp import soloRestartApp
@app.route('/<facility_id>/restart-app', methods=['POST'])
def restartAppWrapper(facility_id) -> flask.Response:
  if swarm_mode:
    return flask.make_response("restart-app endpoint incompatible with swarm mode", 400)
  else:
    return soloRestartApp(facility_id)


from methods.solo.soloKillApp import soloKillApp
from methods.swarm.swarmKillApp import swarmKillApp
@app.route('/<facility_id>/kill-app', methods=['POST'])
def killAppWrapper(facility_id) -> flask.Response:
  if swarm_mode:
    return swarmKillApp(facility_id)
  else:
    return soloKillApp(facility_id)


from methods.solo.soloCreateApp import soloCreateApp
from methods.swarm.swarmCreateApp import swarmCreateApp
@app.route('/<facility_id>/create-app', methods=['POST'])
def createAppWrapper(facility_id) -> flask.Response:
  if swarm_mode:
    return swarmCreateApp(facility_id)
  else:
    return soloCreateApp(facility_id)


from methods.solo.soloDeleteApp import soloDeleteApp
@app.route('/<facility_id>/delete-app', methods=['POST'])
def deleteAppWrapper(facility_id) -> flask.Response:
  if swarm_mode:
    return flask.make_response("delete-app endpoint incompatible with swarm mode", 400)
  else:
    return soloDeleteApp(facility_id)


from methods.solo.soloHardResetApp import soloHardResetApp
@app.route('/<facility_id>/hard-reset-app', methods=['POST'])
def hardResetAppWrapper(facility_id) -> flask.Response:
  if swarm_mode:
    return flask.make_response("hard-reset-app endpoint incompatible with swarm mode", 400)
  else:
    return soloHardResetApp(facility_id)


from methods.solo.soloGetAppNames import soloGetAppNames
from methods.swarm.swarmGetAppNames import swarmGetAppNames
@app.route('/<facility_id>/get-app-names', methods=['GET'])
def getAppNamesWrapper(facility_id) -> flask.Response:
  if swarm_mode:
    return swarmGetAppNames(facility_id)
  else:
    return soloGetAppNames(facility_id)


from methods.solo.soloGetAppStatus import soloGetAppStatus
from methods.swarm.swarmGetAppStatus import swarmGetAppStatus
@app.route('/<facility_id>/get-app-status', methods=['GET'])
def getAppStatusWrapper(facility_id) -> flask.Response:
  if swarm_mode:
    return swarmGetAppStatus(facility_id)
  else:
    return soloGetAppStatus(facility_id)


from methods.solo.soloGetAppStats import soloGetAppStats
from methods.swarm.swarmGetAppStats import swarmGetAppStats
@app.route('/<facility_id>/get-app-stats', methods=['GET'])
def getAppStatsWrapper(facility_id) -> flask.Response:
  if swarm_mode:
    return swarmGetAppStats(facility_id)
  else:
    return soloGetAppStats(facility_id)


from methods.solo.soloGetAppInfo import soloGetAppInfo
from methods.swarm.swarmGetAppInfo import swarmGetAppInfo
@app.route('/<facility_id>/get-app-info', methods=['GET'])
def getAppInfoWrapper(facility_id) -> flask.Response:
  if swarm_mode:
    return swarmGetAppInfo(facility_id)
  else:
    return soloGetAppInfo(facility_id)


from methods.swarm.swarmGetNodeNames import swarmGetNodeNames
@app.route('/<facility_id>/swarm-get-node-names', methods=['GET'])
def getNodeNamesWrapper(facility_id) -> flask.Response:
  if swarm_mode:
    return swarmGetNodeNames(facility_id)
  else:
    return flask.make_response("get-node-names endpoint incompatible with solo mode", 400)

from methods.swarm.swarmGetNodeStatus import swarmGetNodeStatus
@app.route('/<facility_id>/swarm-get-node-status', methods=['GET'])
def getNodeStatusWrapper(facility_id) -> flask.Response:
  if swarm_mode:
    return swarmGetNodeStatus(facility_id)
  else:
    return flask.make_response("get-node-status endpoint incompatible with solo mode", 400)


from methods.swarm.swarmGetNodeInfo import swarmGetNodeInfo
@app.route('/<facility_id>/swarm-get-node-info', methods=['GET'])
def getNodeInfoWrapper(facility_id) -> flask.Response:
  if swarm_mode:
    return swarmGetNodeInfo(facility_id)
  else:
    return flask.make_response("get-node-info endpoint incompatible with solo mode", 400)
  

# AGNOSTIC METHODS ================================================================


from methods.agnostic.getUptimeSummary import getUptimeSummary
@app.route('/<facility_id>/get-uptime-summary', methods=['GET'])
def getUptimeSummaryWrapper(facility_id) -> flask.Response:
  return getUptimeSummary(facility_id)


from methods.agnostic.requestImage import requestImage
@app.route('/<facility_id>/request-image', methods=['POST'])
def requestImageWrapper(facility_id) -> flask.Response:
  return requestImage(facility_id)


from methods.agnostic.getImages import getImages
@app.route('/<facility_id>/get-images', methods=['GET'])
def getImagesWrapper(facility_id) -> flask.Response:
  return getImages(facility_id)


# main
if __name__ == '__main__':
  print("\n\n\n")

  print(" * Checking swarm mode: ", end="")
  swarm_mode = internal_methods.checkSwarmMode()
  print(swarm_mode)

  print(" * Starting logging thread")
  logThread = threading.Thread(target=logger.loggingThreadFunc, daemon=True)
  logThread.start()

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

  completedProcess = internal_methods.subprocessRun("docker ps")
  if completedProcess.returncode != 0:
    print(Style.BRIGHT + Fore.RED + "WARNING: Docker does not appear to be running " + Style.RESET_ALL)

  app.run(port=port)