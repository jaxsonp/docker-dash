from colorama import Fore
from datetime import datetime
import json
from requests import get, post
import subprocess

total_tests = 0
successful_tests = 0

def test(testname:str, method:str, url:str, expected_code:int):
  global total_tests, successful_tests

  start_time = datetime.now()
  total_tests += 1
  print(f"{'{:47.47}'.format(testname):}: ", end='')
  response = None
  if method == "GET":
    response = get(url)
  elif method == "POST":
    response = post(url)
  else:
    print("test error")
    return False

  duration = (datetime.now() - start_time).microseconds // 1000
  if response.status_code == expected_code:
    print(f"{Fore.GREEN}PASS {Fore.RESET}" + f"({duration}ms)".rjust(8))
    successful_tests += 1
    return True
  else:
    print(f"{Fore.RED}FAIL {Fore.RESET}({str(duration).rjust(3)}ms) - expected {expected_code}, got {response.status_code}")
    print("-" * 60)
    print(response.text[:300])
    print("-" * 60)
    return False


if __name__ == "__main__":

  # test parameters
  BASE_URL = "http://127.0.0.1:5000"
  SERVER_ID = "demo"
  USER_NAME = "test"
  IMAGE_NAME = "httpd"
  TEST_IMAGE = "hello-world" # <-- this image should not be installed
  NODE_NAME = "localhost.server2" # <-- this node should already be configured

  APP_NAME = f"{IMAGE_NAME}--{USER_NAME}"

  completedProcess = subprocess.run("docker info --format json", shell=True, capture_output=True)
  SWARM_MODE = json.loads(completedProcess.stdout.decode())["Swarm"]["LocalNodeState"] == "active"

  # install IMAGE_NAME if not already
  subprocess.run(f"docker pull {IMAGE_NAME}", shell=True, capture_output=True)

  def startApp(app_name): subprocess.run(f"docker start {app_name}", shell=True, capture_output=True)
  def killApp(app_name): subprocess.run(f"docker kill {app_name}", shell=True, capture_output=True)
  def removeImage(image): subprocess.run(f"docker rmi {image}", shell=True, capture_output=True)
  def createApp(image, user): subprocess.run(f"docker create --name {image}--{user} {image}", shell=True, capture_output=True)
  def deleteApp(app_name): subprocess.run(f"docker rm {app_name}", shell=True, capture_output=True)

  print("\nStarting testing...")
  start_time = datetime.now()

  print()
  test("Create app - success",                           "POST", f"{BASE_URL}/{SERVER_ID}/create-app?image={IMAGE_NAME}&user={USER_NAME}", 200)
  test("Create app - app already exists",                "POST", f"{BASE_URL}/{SERVER_ID}/create-app?image={IMAGE_NAME}&user={USER_NAME}", 400)
  test("Create app - invalid server ID",                 "POST", f"{BASE_URL}/iaminvalid/create-app?image={IMAGE_NAME}&user={USER_NAME}", 400)
  test("Create app - invalid image name",                "POST", f"{BASE_URL}/{SERVER_ID}/create-app?image=iaminvalid&user={USER_NAME}", 400)
  test("Create app - no image name",                     "POST", f"{BASE_URL}/{SERVER_ID}/create-app?user={USER_NAME}", 400)
  test("Create app - no user name",                      "POST", f"{BASE_URL}/{SERVER_ID}/create-app?image={IMAGE_NAME}", 400)

  if not SWARM_MODE:
    print()
    test("Start app - success",                      "POST", f"{BASE_URL}/{SERVER_ID}/start-app?name={APP_NAME}", 200)
    test("Start app - invalid server ID",            "POST", f"{BASE_URL}/iaminvalid/start-app?name={APP_NAME}", 400)
    test("Start app - invalid app name",             "POST", f"{BASE_URL}/{SERVER_ID}/start-app?name=iaminvalid", 400)
    test("Start app - no app name",                  "POST", f"{BASE_URL}/{SERVER_ID}/start-app", 400)

    print()
    createApp(IMAGE_NAME, USER_NAME + "2")
    createApp(IMAGE_NAME, USER_NAME + "3")
    test("Batch start app",                          "POST", f"{BASE_URL}/{SERVER_ID}/start-app?name={APP_NAME},{APP_NAME}2,{APP_NAME}3", 200)
    test("Batch stop app",                           "POST", f"{BASE_URL}/{SERVER_ID}/stop-app?name={APP_NAME},{APP_NAME}2,{APP_NAME}3", 200)
    deleteApp(APP_NAME + "2")
    deleteApp(APP_NAME + "3")

    print()
    test("Stop app - success",                       "POST", f"{BASE_URL}/{SERVER_ID}/stop-app?name={APP_NAME}", 200)
    test("Stop app - invalid server ID",             "POST", f"{BASE_URL}/iaminvalid/stop-app?name={APP_NAME}", 400)
    test("Stop app - invalid app name",              "POST", f"{BASE_URL}/{SERVER_ID}/stop-app?name=iaminvalid", 400)
    test("Stop app - no app name",                   "POST", f"{BASE_URL}/{SERVER_ID}/stop-app", 400)
    startApp(APP_NAME)

    print()
    test("Pause app - success",                      "POST", f"{BASE_URL}/{SERVER_ID}/pause-app?name={APP_NAME}", 200)
    test("Pause app - invalid server ID",            "POST", f"{BASE_URL}/iaminvalid/pause-app?name={APP_NAME}", 400)
    test("Pause app - invalid app name",             "POST", f"{BASE_URL}/{SERVER_ID}/pause-app?name=iaminvalid", 400)
    test("Pause app - no app name",                  "POST", f"{BASE_URL}/{SERVER_ID}/pause-app", 400)

    print()
    test("Unpause app - success",                    "POST", f"{BASE_URL}/{SERVER_ID}/unpause-app?name={APP_NAME}", 200)
    test("Unpause app - invalid server ID",          "POST", f"{BASE_URL}/iaminvalid/unpause-app?name={APP_NAME}", 400)
    test("Unpause app - invalid app name",           "POST", f"{BASE_URL}/{SERVER_ID}/unpause-app?name=iaminvalid", 400)
    test("Unpause app - no app name",                "POST", f"{BASE_URL}/{SERVER_ID}/unpause-app", 400)

    print()
    test("Restart app - success",                    "POST", f"{BASE_URL}/{SERVER_ID}/restart-app?name={APP_NAME}", 200)
    test("Restart app - invalid server ID",          "POST", f"{BASE_URL}/iaminvalid/restart-app?name={APP_NAME}", 400)
    test("Restart app - invalid app name",           "POST", f"{BASE_URL}/{SERVER_ID}/restart-app?name=iaminvalid", 400)
    test("Restart app - no app name",                "POST", f"{BASE_URL}/{SERVER_ID}/restart-app", 400)

  print()
  test("Get app names - success",                  "GET", f"{BASE_URL}/{SERVER_ID}/get-users", 200)
  test("Get app names - invalid server ID",        "GET", f"{BASE_URL}/iaminvalid/get-users", 400)

  print()
  test("Get app status - success",                 "GET", f"{BASE_URL}/{SERVER_ID}/get-app-status", 200)
  test("Get app status - success (specific app)",  "GET", f"{BASE_URL}/{SERVER_ID}/get-app-status?name={APP_NAME}", 200)
  test("Get app status - invalid server ID",       "GET", f"{BASE_URL}/iaminvalid/get-app-status?name={APP_NAME}", 400)
  test("Get app status - invalid app name",        "GET", f"{BASE_URL}/{SERVER_ID}/get-app-status?name=iaminvalid", 400)

  print()
  test("Get app stats - success",                 "GET", f"{BASE_URL}/{SERVER_ID}/get-app-stats", 200)
  test("Get app stats - success (specific app)",  "GET", f"{BASE_URL}/{SERVER_ID}/get-app-stats?name={APP_NAME}", 200)
  test("Get app stats - invalid server ID",       "GET", f"{BASE_URL}/iaminvalid/get-app-stats?name={APP_NAME}", 400)
  test("Get app stats - invalid app name",        "GET", f"{BASE_URL}/{SERVER_ID}/get-app-stats?name=iaminvalid", 400)

  print()
  test("Get app info - success",                   "GET", f"{BASE_URL}/{SERVER_ID}/get-app-info?name={APP_NAME}", 200)
  test("Get app info - invalid server ID",         "GET", f"{BASE_URL}/iaminvalid/get-app-info?name={APP_NAME}", 400)
  test("Get app info - invalid app name",          "GET", f"{BASE_URL}/{SERVER_ID}/get-app-info?name=iaminvalid", 400)
  test("Get app info - no app name",               "GET", f"{BASE_URL}/{SERVER_ID}/get-app-info", 400)
  
  print()
  test("Kill app - success",                       "POST", f"{BASE_URL}/{SERVER_ID}/kill-app?name={APP_NAME}", 200)
  test("Kill app - invalid server ID",             "POST", f"{BASE_URL}/iaminvalid/kill-app?name={APP_NAME}", 400)
  test("Kill app - invalid app name",              "POST", f"{BASE_URL}/{SERVER_ID}/kill-app?name=iaminvalid", 400)
  test("Kill app - no app name",                   "POST", f"{BASE_URL}/{SERVER_ID}/kill-app", 400)
  startApp(APP_NAME)

  print()
  test("Get node names - success",                       "GET", f"{BASE_URL}/{SERVER_ID}/get-node-names", 200)
  test("Get node names - invalid facility ID",           "GET", f"{BASE_URL}/iaminvalid/get-node-names", 400)

  print()
  test("Get node status - success",                      "GET", f"{BASE_URL}/{SERVER_ID}/get-node-status", 200)
  test("Get node status - invalid facility ID",          "GET", f"{BASE_URL}/iaminvalid/get-node-status?hostname={NODE_NAME}", 400)

  if SWARM_MODE:

    test("Get node status - success (specific node)",      "GET", f"{BASE_URL}/{SERVER_ID}/get-node-status?hostname={NODE_NAME}", 200)
    test("Get node status - invalid hostname",             "GET", f"{BASE_URL}/{SERVER_ID}/get-node-status?hostname=iaminvalid", 400)

    print()
    test("Get node info - success",                        "GET", f"{BASE_URL}/{SERVER_ID}/get-node-info?hostname={NODE_NAME}", 200)
    test("Get node info - invalid facility ID",            "GET", f"{BASE_URL}/iaminvalid/get-node-info?hostname={NODE_NAME}", 400)
    test("Get node info - invalid app name",               "GET", f"{BASE_URL}/{SERVER_ID}/get-node-info?hostname=iaminvalid", 400)
    test("Get node info - no app name",                    "GET", f"{BASE_URL}/{SERVER_ID}/get-node-info", 400)

  print()
  test("Get uptime summary - success",                   "GET", f"{BASE_URL}/{SERVER_ID}/get-uptime-summary?name={APP_NAME}&duration=day", 200)
  test("Get uptime summary - invalid server ID",         "GET", f"{BASE_URL}/iaminvalid/get-uptime-summary?name={APP_NAME}&duration=day", 400)
  test("Get uptime summary - invalid app name",          "GET", f"{BASE_URL}/{SERVER_ID}/get-uptime-summary?name=iaminvalid&duration=day", 400)
  test("Get uptime summary - invalid duration",          "GET", f"{BASE_URL}/{SERVER_ID}/get-uptime-summary?name={APP_NAME}&duration=bad", 400)
  test("Get uptime summary - no duration",               "GET", f"{BASE_URL}/{SERVER_ID}/get-uptime-summary?name={APP_NAME}", 400)

  print()
  test("Request Image - success",                        "POST", f"{BASE_URL}/{SERVER_ID}/request-image?image={TEST_IMAGE}", 200)
  test("Request Image - invalid server ID",              "POST", f"{BASE_URL}/iaminvalid/request-image?image={TEST_IMAGE}", 400)
  test("Request Image - invalid image name",             "POST", f"{BASE_URL}/{SERVER_ID}/request-image?image=iaminvalid", 400)
  test("Request Image - no image name",                  "POST", f"{BASE_URL}/{SERVER_ID}/request-image?", 400)
  
  print()
  test("Get images - success",                           "GET", f"{BASE_URL}/{SERVER_ID}/get-images", 200)
  test("Get images - invalid server ID",                 "GET", f"{BASE_URL}/iaminvalid/get-images", 400)

  removeImage(TEST_IMAGE)

  if not SWARM_MODE:
    print()
    test("Delete app - invalid server ID",           "POST", f"{BASE_URL}/iaminvalid/delete-app?name={APP_NAME}", 400)
    test("Delete app - invalid app name",            "POST", f"{BASE_URL}/{SERVER_ID}/delete-app?name=iaminvalid", 400)
    test("Delete app - no app name",                 "POST", f"{BASE_URL}/{SERVER_ID}/delete-app", 400)
    test("Delete app - success",                     "POST", f"{BASE_URL}/{SERVER_ID}/delete-app?name={APP_NAME}", 200)

  duration = datetime.now() - start_time
  print(f"\n\nCompleted testing, {successful_tests}/{total_tests} tests successful (took {round(duration.total_seconds(), 2)} seconds)")
