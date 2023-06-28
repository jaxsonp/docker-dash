#from flask import Flask, request, Response
import flask
import threading

import logger


app = flask.Flask(__name__)


from methods.startApp import startApp
@app.route('/<facility_id>/start-app', methods=['POST'])
def startAppWrapper(facility_id) -> flask.Response:
  return startApp(facility_id)


from methods.stopApp import stopApp
@app.route('/<facility_id>/stop-app', methods=['POST'])
def stopAppWrapper(facility_id) -> flask.Response:
  return stopApp(facility_id)


from methods.pauseApp import pauseApp
@app.route('/<facility_id>/pause-app', methods=['POST'])
def pauseAppWrapper(facility_id) -> flask.Response:
  return pauseApp(facility_id)


from methods.unpauseApp import unpauseApp
@app.route('/<facility_id>/unpause-app', methods=['POST'])
def unpauseAppWrapper(facility_id) -> flask.Response:
  return unpauseApp(facility_id)


from methods.restartApp import restartApp
@app.route('/<facility_id>/restart-app', methods=['POST'])
def restartAppWrapper(facility_id) -> flask.Response:
  return restartApp(facility_id)


from methods.killApp import killApp
@app.route('/<facility_id>/kill-app', methods=['POST'])
def killAppWrapper(facility_id) -> flask.Response:
  return killApp(facility_id)


from methods.deleteApp import deleteApp
@app.route('/<facility_id>/delete-app', methods=['POST'])
def deleteAppWrapper(facility_id) -> flask.Response:
  return deleteApp(facility_id)


from methods.hardResetApp import hardResetApp
@app.route('/<facility_id>/hard-reset-app', methods=['POST'])
def hardResetAppWrapper(facility_id) -> flask.Response:
  return hardResetApp(facility_id)


from methods.getAppNames import getAppNames
@app.route('/<facility_id>/get-app-names', methods=['GET'])
def getAppNamesWrapper(facility_id) -> flask.Response:
  return getAppNames(facility_id)


from methods.getAppStatus import getAppStatus
@app.route('/<facility_id>/get-app-status', methods=['GET'])
def getAppStatusWrapper(facility_id) -> flask.Response:
  return getAppStatus(facility_id)


from methods.getAppStats import getAppStats
@app.route('/<facility_id>/get-app-stats', methods=['GET'])
def getAppStatsWrapper(facility_id) -> flask.Response:
  return getAppStats(facility_id)


from methods.getAppInfo import getAppInfo
@app.route('/<facility_id>/get-app-info', methods=['GET'])
def getAppInfoWrapper(facility_id) -> flask.Response:
  return getAppInfo(facility_id)


from methods.getUptimeSummary import getUptimeSummary
@app.route('/<facility_id>/get-uptime-summary', methods=['GET'])
def getUptimeSummaryWrapper(facility_id) -> flask.Response:
  return getUptimeSummary(facility_id)


from methods.requestImage import requestImage
@app.route('/<facility_id>/request-image', methods=['POST'])
def requestImageWrapper(facility_id):
  return requestImage(facility_id)


from methods.getImages import getImages
@app.route('/<facility_id>/get-images', methods=['GET'])
def getImagesWrapper(facility_id):
  return getImages(facility_id)


# SWARM METHODS ================================================================


from methods.swarmCreateApp import swarmCreateApp
@app.route('/<facility_id>/swarm-create-app', methods=['POST'])
def swarmCreateAppWrapper(facility_id) -> flask.Response:
  return swarmCreateApp(facility_id)


from methods.swarmGetAppInfo import swarmGetAppInfo
@app.route('/<facility_id>/swarm-get-app-info', methods=['GET'])
def swarmGetAppInfoWrapper(facility_id) -> flask.Response:
  return swarmGetAppInfo(facility_id)


from methods.swarmGetAppNames import swarmGetAppNames
@app.route('/<facility_id>/swarm-get-app-names', methods=['GET'])
def swarmGetAppNamesWrapper(facility_id) -> flask.Response:
  return swarmGetAppNames(facility_id)


from methods.swarmGetAppStats import swarmGetAppStats
@app.route('/<facility_id>/swarm-get-app-status', methods=['GET'])
def swarmGetAppStatsWrapper(facility_id) -> flask.Response:
  return swarmGetAppStats(facility_id)


from methods.swarmGetAppStatus import swarmGetAppStatus
@app.route('/<facility_id>/swarm-get-app-status', methods=['GET'])
def swarmGetAppStatusWrapper(facility_id) -> flask.Response:
  return swarmGetAppStatus(facility_id)


from methods.swarmKillApp import swarmKillApp
@app.route('/<facility_id>/swarm-kill-app', methods=['POST'])
def swarmKillAppWrapper(facility_id) -> flask.Response:
  return swarmKillApp(facility_id)


if __name__ == '__main__':
  print("\n\n\n")

  print("Starting logging thread")
  logThread = threading.Thread(target=logger.loggingThreadFunc, daemon=True)
  logThread.start()
  print("Starting flask server")
  app.run()