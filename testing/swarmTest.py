from requests import get, post
from colorama import Fore
from datetime import datetime
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
  FACILITY_ID = "demo"
  USER_NAME = "test"
  IMAGE_NAME = "httpd" # <-- this should already be installed
  TEST_IMAGE = "hello-world" # <-- this one should not be installed
  NODE_NAME = "localhost.server2"

  APP_NAME = f"{IMAGE_NAME}--{USER_NAME}"

  def removeImage(image): subprocess.run(f"docker rmi {image}", shell=True, capture_output=True)
  def createApp(image, user): subprocess.run(f"docker service create --name {image}--{user} --mode replicated-job -d {image}", shell=True, capture_output=True)
  def deleteApp(app_name): subprocess.run(f"docker service rm {app_name}", shell=True, capture_output=True)

  print("\nStarting swarm testing...")
  start_time = datetime.now()

  print()
  test("Create app - success",                           "POST", f"{BASE_URL}/{FACILITY_ID}/swarm-create-app?image={IMAGE_NAME}&user={USER_NAME}", 200)
  test("Create app - app already exists",                "POST", f"{BASE_URL}/{FACILITY_ID}/swarm-create-app?image={IMAGE_NAME}&user={USER_NAME}", 400)
  test("Create app - invalid facility ID",               "POST", f"{BASE_URL}/iaminvalid/swarm-create-app?image={IMAGE_NAME}&user={USER_NAME}", 400)
  test("Create app - invalid image name",                "POST", f"{BASE_URL}/{FACILITY_ID}/swarm-create-app?image=iaminvalid&user={USER_NAME}", 400)
  test("Create app - no image name",                     "POST", f"{BASE_URL}/{FACILITY_ID}/swarm-create-app?user={USER_NAME}", 400)
  test("Create app - no user name",                      "POST", f"{BASE_URL}/{FACILITY_ID}/swarm-create-app?image={IMAGE_NAME}", 400)
  createApp(IMAGE_NAME, USER_NAME+"2")
  createApp(IMAGE_NAME, USER_NAME+"3")
  
  print()
  test("Get app names - success",                        "GET", f"{BASE_URL}/{FACILITY_ID}/swarm-get-app-names", 200)
  test("Get app names - invalid facility ID",            "GET", f"{BASE_URL}/iaminvalid/swarm-get-app-names", 400)

  print()
  test("Get service status - success",                   "GET", f"{BASE_URL}/{FACILITY_ID}/swarm-get-app-status", 200)
  test("Get service status - success (specific app)",    "GET", f"{BASE_URL}/{FACILITY_ID}/swarm-get-app-status?name={APP_NAME}", 200)
  test("Get service status - invalid facility ID",       "GET", f"{BASE_URL}/iaminvalid/swarm-get-app-status?name={APP_NAME}", 400)
  test("Get service status - invalid app name",          "GET", f"{BASE_URL}/{FACILITY_ID}/swarm-get-app-status?name=iaminvalid", 400)

  print()
  test("Get service stats - success",                    "GET", f"{BASE_URL}/{FACILITY_ID}/swarm-get-app-stats", 200)
  test("Get service stats - success (specific app)",     "GET", f"{BASE_URL}/{FACILITY_ID}/swarm-get-app-stats?name={APP_NAME}", 200)
  test("Get service stats - invalid facility ID",        "GET", f"{BASE_URL}/iaminvalid/swarm-get-app-stats?name={APP_NAME}", 400)
  test("Get service stats - invalid app name",           "GET", f"{BASE_URL}/{FACILITY_ID}/swarm-get-app-stats?name=iaminvalid", 400)
  deleteApp(f"{IMAGE_NAME}--{USER_NAME}2")
  deleteApp(f"{IMAGE_NAME}--{USER_NAME}3")

  print()
  test("Get service info - success",                     "GET", f"{BASE_URL}/{FACILITY_ID}/swarm-get-app-info?name={APP_NAME}", 200)
  test("Get service info - invalid facility ID",         "GET", f"{BASE_URL}/iaminvalid/swarm-get-app-info?name={APP_NAME}", 400)
  test("Get service info - invalid app name",            "GET", f"{BASE_URL}/{FACILITY_ID}/swarm-get-app-info?name=iaminvalid", 400)
  test("Get service info - no app name",                 "GET", f"{BASE_URL}/{FACILITY_ID}/swarm-get-app-info", 400)

  print()
  test("Kill service - invalid facility ID",             "POST", f"{BASE_URL}/iaminvalid/swarm-kill-app?name={APP_NAME}", 400)
  test("Kill service - invalid app name",                "POST", f"{BASE_URL}/{FACILITY_ID}/swarm-kill-app?name=iaminvalid", 400)
  test("Kill service - no app name",                     "POST", f"{BASE_URL}/{FACILITY_ID}/swarm-kill-app", 400)
  test("Kill service - success",                         "POST", f"{BASE_URL}/{FACILITY_ID}/swarm-kill-app?name={APP_NAME}", 200)

  print()
  test("Get node names - success",                       "GET", f"{BASE_URL}/{FACILITY_ID}/swarm-get-node-names", 200)
  test("Get node names - invalid facility ID",           "GET", f"{BASE_URL}/iaminvalid/swarm-get-node-names", 400)

  print()
  test("Get node status - success",                      "GET", f"{BASE_URL}/{FACILITY_ID}/swarm-get-node-status", 200)
  test("Get node status - success (specific node)",      "GET", f"{BASE_URL}/{FACILITY_ID}/swarm-get-node-status?hostname={NODE_NAME}", 200)
  test("Get node status - invalid facility ID",          "GET", f"{BASE_URL}/iaminvalid/swarm-get-node-status?hostname={NODE_NAME}", 400)
  test("Get node status - invalid app name",             "GET", f"{BASE_URL}/{FACILITY_ID}/swarm-get-node-status?hostname=iaminvalid", 400)

  print()
  test("Get node info - success",                        "GET", f"{BASE_URL}/{FACILITY_ID}/swarm-get-node-info?hostname={NODE_NAME}", 200)
  test("Get node info - invalid facility ID",            "GET", f"{BASE_URL}/iaminvalid/swarm-get-node-info?hostname={NODE_NAME}", 400)
  test("Get node info - invalid app name",               "GET", f"{BASE_URL}/{FACILITY_ID}/swarm-get-node-info?hostname=iaminvalid", 400)
  test("Get node info - no app name",                    "GET", f"{BASE_URL}/{FACILITY_ID}/swarm-get-node-info", 400)
  
  print()
  test("Request Image - success",                        "POST", f"{BASE_URL}/{FACILITY_ID}/request-image?image={TEST_IMAGE}", 200)
  test("Request Image - invalid facility ID",            "POST", f"{BASE_URL}/iaminvalid/request-image?image={TEST_IMAGE}", 400)
  test("Request Image - invalid image name",             "POST", f"{BASE_URL}/{FACILITY_ID}/request-image?image=iaminvalid", 400)
  test("Request Image - no image name",                  "POST", f"{BASE_URL}/{FACILITY_ID}/request-image?", 400)
  
  print()
  test("Get images - success",                           "GET", f"{BASE_URL}/{FACILITY_ID}/get-images", 200)
  test("Get images - invalid facility ID",               "GET", f"{BASE_URL}/iaminvalid/get-images", 400)
  removeImage(TEST_IMAGE)

  

  duration = datetime.now() - start_time
  print(f"\n\nCompleted testing, {successful_tests}/{total_tests} tests successful (took {round(duration.total_seconds(), 2)} seconds)")
