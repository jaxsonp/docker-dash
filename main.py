import sys
import flask
import threading
from colorama import Fore, Style
from methods import internal_methods

import logger


app = flask.Flask(__name__)


@app.route('/')
def helper() -> flask.Response:
  with open("root_page.txt", "r") as f:
    return flask.Response(f.read(), mimetype='text/plain')


from methods.solo.startApp import startApp
@app.route('/<facility_id>/start-app', methods=['POST'])
def startAppWrapper(facility_id) -> flask.Response:
  return startApp(facility_id)


from methods.solo.stopApp import stopApp
@app.route('/<facility_id>/stop-app', methods=['POST'])
def stopAppWrapper(facility_id) -> flask.Response:
  return stopApp(facility_id)


from methods.solo.pauseApp import pauseApp
@app.route('/<facility_id>/pause-app', methods=['POST'])
def pauseAppWrapper(facility_id) -> flask.Response:
  return pauseApp(facility_id)


from methods.solo.unpauseApp import unpauseApp
@app.route('/<facility_id>/unpause-app', methods=['POST'])
def unpauseAppWrapper(facility_id) -> flask.Response:
  return unpauseApp(facility_id)


from methods.solo.restartApp import restartApp
@app.route('/<facility_id>/restart-app', methods=['POST'])
def restartAppWrapper(facility_id) -> flask.Response:
  return restartApp(facility_id)


from methods.solo.killApp import killApp
@app.route('/<facility_id>/kill-app', methods=['POST'])
def killAppWrapper(facility_id) -> flask.Response:
  return killApp(facility_id)


from methods.solo.createApp import createApp
@app.route('/<facility_id>/create-app', methods=['POST'])
def createAppWrapper(facility_id) -> flask.Response:
  return createApp(facility_id)


from methods.solo.deleteApp import deleteApp
@app.route('/<facility_id>/delete-app', methods=['POST'])
def deleteAppWrapper(facility_id) -> flask.Response:
  return deleteApp(facility_id)


from methods.solo.hardResetApp import hardResetApp
@app.route('/<facility_id>/hard-reset-app', methods=['POST'])
def hardResetAppWrapper(facility_id) -> flask.Response:
  return hardResetApp(facility_id)


from methods.solo.getAppNames import getAppNames
@app.route('/<facility_id>/get-app-names', methods=['GET'])
def getAppNamesWrapper(facility_id) -> flask.Response:
  return getAppNames(facility_id)


from methods.solo.getAppStatus import getAppStatus
@app.route('/<facility_id>/get-app-status', methods=['GET'])
def getAppStatusWrapper(facility_id) -> flask.Response:
  return getAppStatus(facility_id)


from methods.solo.getAppStats import getAppStats
@app.route('/<facility_id>/get-app-stats', methods=['GET'])
def getAppStatsWrapper(facility_id) -> flask.Response:
  return getAppStats(facility_id)


from methods.solo.getAppInfo import getAppInfo
@app.route('/<facility_id>/get-app-info', methods=['GET'])
def getAppInfoWrapper(facility_id) -> flask.Response:
  return getAppInfo(facility_id)


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


# SWARM METHODS ================================================================


from methods.swarm.swarmCreateApp import swarmCreateApp
@app.route('/<facility_id>/swarm-create-app', methods=['POST'])
def swarmCreateAppWrapper(facility_id) -> flask.Response:
  return swarmCreateApp(facility_id)


from methods.swarm.swarmGetAppInfo import swarmGetAppInfo
@app.route('/<facility_id>/swarm-get-app-info', methods=['GET'])
def swarmGetAppInfoWrapper(facility_id) -> flask.Response:
  return swarmGetAppInfo(facility_id)


from methods.swarm.swarmGetAppNames import swarmGetAppNames
@app.route('/<facility_id>/swarm-get-app-names', methods=['GET'])
def swarmGetAppNamesWrapper(facility_id) -> flask.Response:
  return swarmGetAppNames(facility_id)


from methods.swarm.swarmGetAppStats import swarmGetAppStats
@app.route('/<facility_id>/swarm-get-app-stats', methods=['GET'])
def swarmGetAppStatsWrapper(facility_id) -> flask.Response:
  return swarmGetAppStats(facility_id)


from methods.swarm.swarmGetAppStatus import swarmGetAppStatus
@app.route('/<facility_id>/swarm-get-app-status', methods=['GET'])
def swarmGetAppStatusWrapper(facility_id) -> flask.Response:
  return swarmGetAppStatus(facility_id)


from methods.swarm.swarmKillApp import swarmKillApp
@app.route('/<facility_id>/swarm-kill-app', methods=['POST'])
def swarmKillAppWrapper(facility_id) -> flask.Response:
  return swarmKillApp(facility_id)


from methods.swarm.swarmGetNodeNames import swarmGetNodeNames
@app.route('/<facility_id>/swarm-get-node-names', methods=['GET'])
def swarmGetNodeNamesWrapper(facility_id) -> flask.Response:
  return swarmGetNodeNames(facility_id)


from methods.swarm.swarmGetNodeStatus import swarmGetNodeStatus
@app.route('/<facility_id>/swarm-get-node-status', methods=['GET'])
def swarmGetNodeStatusWrapper(facility_id) -> flask.Response:
  return swarmGetNodeStatus(facility_id)


from methods.swarm.swarmGetNodeInfo import swarmGetNodeInfo
@app.route('/<facility_id>/swarm-get-node-info', methods=['GET'])
def swarmGetNodeInfoWrapper(facility_id) -> flask.Response:
  return swarmGetNodeInfo(facility_id)



# main
if __name__ == '__main__':
  print("\n\n\n")

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