from requests import get, post
from colorama import Fore, Style
from datetime import datetime
import subprocess

totalTests = 0
successfulTests = 0

def test(testname:str, method:str, url:str, expectedCode:int):
  global totalTests, successfulTests
  totalTests += 1
  print(f"{'{:50.50}'.format(testname):}: ", end='')
  response = None
  if method == "GET":
    response = get(url)
  elif method == "POST":
    response = post(url)
  else:
    print("test error")
    return False

  if response.status_code == expectedCode:
    print(Fore.GREEN + "SUCCESS", Fore.RESET)
    successfulTests += 1
    return True
  else:
    print(Fore.RED + "FAIL", Fore.RESET + f"- expected {expectedCode}, got {response.status_code}")
    print("-" * 60)
    print(response.text[:300])
    print("-" * 60)
    return False


if __name__ == "__main__":

  #read secrets.txt
  with open("testing/secrets.txt", "r") as f:
    lines = [line.split("=")[1] for line in f.readlines()]
  BASE_URL = lines[0].strip()
  FACILITY_ID = lines[1].strip()
  APP_NAME = lines[2].strip()
  def startApp():
    post(f"{BASE_URL}/{FACILITY_ID}/startApp?name={APP_NAME}")

  def killApp():
    post(f"{BASE_URL}/{FACILITY_ID}/killApp?name={APP_NAME}")

  # getting image name
  IMAGE_NAME = ""
  completedResponse = subprocess.run(f"docker ps -a --filter name={APP_NAME} --format \"{{{{.Names}}}} {{{{.Image}}}}\"", capture_output=True)
  nameList = [tuple(line.split()) for line in completedResponse.stdout.decode().split("\n")[:-1]]
  for name, image in nameList:
    if name == APP_NAME:
      IMAGE_NAME = image
      break

  print("\nStarting testing...")
  startTime = datetime.now()

  killApp()
  print()
  test("Start container - success",                      "POST", f"{BASE_URL}/{FACILITY_ID}/startApp?name={APP_NAME}",    200)
  test("Start container - invalid facility ID",          "POST", f"{BASE_URL}/iaminvalid/startApp?name={APP_NAME}",       400)
  test("Start container - invalid app name",             "POST", f"{BASE_URL}/{FACILITY_ID}/startApp?name=iaminvalid",    400)
  test("Start container - no app name",                  "POST", f"{BASE_URL}/{FACILITY_ID}/startApp",                    400)

  print()
  test("Stop container - success",                       "POST", f"{BASE_URL}/{FACILITY_ID}/stopApp?name={APP_NAME}",     200)
  test("Stop container - invalid facility ID",           "POST", f"{BASE_URL}/iaminvalid/stopApp?name={APP_NAME}",        400)
  test("Stop container - invalid app name",              "POST", f"{BASE_URL}/{FACILITY_ID}/stopApp?name=iaminvalid",     400)
  test("Stop container - no app name",                   "POST", f"{BASE_URL}/{FACILITY_ID}/stopApp",                     400)
  startApp()

  print()
  test("Pause container - success",                      "POST", f"{BASE_URL}/{FACILITY_ID}/pauseApp?name={APP_NAME}",    200)
  test("Pause container - invalid facility ID",          "POST", f"{BASE_URL}/iaminvalid/pauseApp?name={APP_NAME}",       400)
  test("Pause container - invalid app name",             "POST", f"{BASE_URL}/{FACILITY_ID}/pauseApp?name=iaminvalid",    400)
  test("Pause container - no app name",                  "POST", f"{BASE_URL}/{FACILITY_ID}/pauseApp",                    400)

  print()
  test("Unpause container - success",                    "POST", f"{BASE_URL}/{FACILITY_ID}/unpauseApp?name={APP_NAME}",  200)
  test("Unpause container - invalid facility ID",        "POST", f"{BASE_URL}/iaminvalid/unpauseApp?name={APP_NAME}",     400)
  test("Unpause container - invalid app name",           "POST", f"{BASE_URL}/{FACILITY_ID}/unpauseApp?name=iaminvalid",  400)
  test("Unpause container - no app name",                "POST", f"{BASE_URL}/{FACILITY_ID}/unpauseApp",                  400)

  print()
  test("Restart container - success",                    "POST", f"{BASE_URL}/{FACILITY_ID}/restartApp?name={APP_NAME}",  200)
  test("Restart container - invalid facility ID",        "POST", f"{BASE_URL}/iaminvalid/restartApp?name={APP_NAME}",     400)
  test("Restart container - invalid app name",           "POST", f"{BASE_URL}/{FACILITY_ID}/restartApp?name=iaminvalid",  400)
  test("Restart container - no app name",                "POST", f"{BASE_URL}/{FACILITY_ID}/restartApp",                  400)

  print()
  test("Kill container - success",                       "POST", f"{BASE_URL}/{FACILITY_ID}/killApp?name={APP_NAME}",     200)
  test("Kill container - invalid facility ID",           "POST", f"{BASE_URL}/iaminvalid/killApp?name={APP_NAME}",        400)
  test("Kill container - invalid app name",              "POST", f"{BASE_URL}/{FACILITY_ID}/killApp?name=iaminvalid",     400)
  test("Kill container - no app name",                   "POST", f"{BASE_URL}/{FACILITY_ID}/killApp",                     400)
  startApp()

  print()
  test("Get container names - success",                  "GET", f"{BASE_URL}/{FACILITY_ID}/getAppNames",                  200)
  test("Get container names - invalid facility ID",      "GET", f"{BASE_URL}/iaminvalid/getAppNames",                     400)

  print()
  test("Get container status - success",                 "GET", f"{BASE_URL}/{FACILITY_ID}/getAppStatus",                 200)
  test("Get container status - success (specific app)",  "GET", f"{BASE_URL}/{FACILITY_ID}/getAppStatus?name={APP_NAME}", 200)
  test("Get container status - invalid facility ID",     "GET", f"{BASE_URL}/iaminvalid/getAppStatus?name={APP_NAME}",    400)
  test("Get container status - invalid app name",        "GET", f"{BASE_URL}/{FACILITY_ID}/getAppStatus?name=iaminvalid", 400)

  print()
  test("Get container info - success",                   "GET", f"{BASE_URL}/{FACILITY_ID}/getAppInfo?name={APP_NAME}",   200)
  test("Get container info - invalid facility ID",       "GET", f"{BASE_URL}/iaminvalid/getAppInfo?name={APP_NAME}",      400)
  test("Get container info - invalid app name",          "GET", f"{BASE_URL}/{FACILITY_ID}/getAppInfo?name=iaminvalid",   400)
  test("Get container info - no app name",               "GET", f"{BASE_URL}/{FACILITY_ID}/getAppInfo",                   400)

  print()
  test("Get health summary - success",                   "GET", f"{BASE_URL}/{FACILITY_ID}/getHealthSummary?name={APP_NAME}&duration=day", 200)
  test("Get health summary - invalid facility ID",       "GET", f"{BASE_URL}/iaminvalid/getHealthSummary?name={APP_NAME}&duration=day",    400)
  test("Get health summary - invalid app name",          "GET", f"{BASE_URL}/{FACILITY_ID}/getHealthSummary?name=iaminvalid&duration=day", 400)
  test("Get health summary - invalid duration",          "GET", f"{BASE_URL}/{FACILITY_ID}/getHealthSummary?name={APP_NAME}&duration=bad", 400)
  test("Get health summary - no duration",               "GET", f"{BASE_URL}/{FACILITY_ID}/getHealthSummary?name={APP_NAME}",              400)

  print()
  test("Get images - success",                           "GET", f"{BASE_URL}/{FACILITY_ID}/getImages",                   200)
  test("Get images - invalid facility ID",               "GET", f"{BASE_URL}/iaminvalid/getImages",                      400)

  # put delete container here

  print()
  test("Create app - success",                           "POST", f"{BASE_URL}/{FACILITY_ID}/createApp?image={IMAGE_NAME}", 200)
  test("Create app - app already exists",                "POST", f"{BASE_URL}/{FACILITY_ID}/createApp?image={IMAGE_NAME}", 200)
  test("Create app - invalid facility ID",               "POST", f"{BASE_URL}/iaminvalid/createApp?image={IMAGE_NAME}", 400)
  test("Create app - invalid image name",                "POST", f"{BASE_URL}/{FACILITY_ID}/createApp?image=iaminvalid", 400)
  test("Create app - no image name",                     "POST", f"{BASE_URL}/{FACILITY_ID}/createApp?", 400)

  testDuration = datetime.now() - startTime
  print(f"\n\nCompleted testing, {successfulTests}/{totalTests} tests successful (took {round(testDuration.total_seconds(), 2)} seconds)")
