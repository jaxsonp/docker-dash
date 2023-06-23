#from flask import Flask, request, Response
import flask
import threading

import logger


app = flask.Flask(__name__)


from methods.startApp import startApp
@app.route('/<facility_id>/startApp', methods=['POST'])
def startAppWrapper(facility_id) -> flask.Response:
  return startApp(facility_id)


from methods.stopApp import stopApp
@app.route('/<facility_id>/stopApp', methods=['POST'])
def stopAppWrapper(facility_id) -> flask.Response:
  return stopApp(facility_id)


from methods.pauseApp import pauseApp
@app.route('/<facility_id>/pauseApp', methods=['POST'])
def pauseAppWrapper(facility_id) -> flask.Response:
  return pauseApp(facility_id)


from methods.unpauseApp import unpauseApp
@app.route('/<facility_id>/unpauseApp', methods=['POST'])
def unpauseAppWrapper(facility_id) -> flask.Response:
  return unpauseApp(facility_id)


from methods.restartApp import restartApp
@app.route('/<facility_id>/restartApp', methods=['POST'])
def restartAppWrapper(facility_id) -> flask.Response:
  return restartApp(facility_id)


from methods.killApp import killApp
@app.route('/<facility_id>/killApp', methods=['POST'])
def killAppWrapper(facility_id) -> flask.Response:
  return killApp(facility_id)


from methods.createApp import createApp
@app.route('/<facility_id>/createApp', methods=['POST'])
def createAppWrapper(facility_id) -> flask.Response:
  return createApp(facility_id)


from methods.deleteApp import deleteApp
@app.route('/<facility_id>/deleteApp', methods=['POST'])
def deleteAppWrapper(facility_id) -> flask.Response:
  return deleteApp(facility_id)


from methods.hardResetApp import hardResetApp
@app.route('/<facility_id>/hardResetApp', methods=['POST'])
def hardResetAppWrapper(facility_id) -> flask.Response:
  return hardResetApp(facility_id)


from methods.getAppNames import getAppNames
@app.route('/<facility_id>/getAppNames', methods=['GET'])
def getAppNamesWrapper(facility_id) -> flask.Response:
  return getAppNames(facility_id)


from methods.getAppStatus import getAppStatus
@app.route('/<facility_id>/getAppStatus', methods=['GET'])
def getAppStatusWrapper(facility_id) -> flask.Response:
  return getAppStatus(facility_id)


from methods.getAppStats import getAppStats
@app.route('/<facility_id>/getAppStats', methods=['GET'])
def getAppStatsWrapper(facility_id) -> flask.Response:
  return getAppStats(facility_id)


from methods.getAppInfo import getAppInfo
@app.route('/<facility_id>/getAppInfo', methods=['GET'])
def getAppInfoWrapper(facility_id) -> flask.Response:
  return getAppInfo(facility_id)


from methods.getUptimeSummary import getUptimeSummary
@app.route('/<facility_id>/getUptimeSummary', methods=['GET'])
def getUptimeSummaryWrapper(facility_id) -> flask.Response:
  return getUptimeSummary(facility_id)


from methods.requestImage import requestImage
@app.route('/<facility_id>/requestImage', methods=['POST'])
def requestImageWrapper(facility_id):
  return requestImage(facility_id)


from methods.getImages import getImages
@app.route('/<facility_id>/getImages', methods=['GET'])
def getImagesWrapper(facility_id):
  return getImages(facility_id)


if __name__ == '__main__':
  print("\n\n\n")

  print("Starting logging thread")
  logThread = threading.Thread(target=logger.loggingThreadFunc, daemon=True)
  logThread.start()
  print("Starting flask server")
  app.run()