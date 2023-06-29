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
    print(f"{Fore.GREEN}SUCCESS {Fore.RESET}" + f"({duration}ms)".rjust(8))
    successful_tests += 1
    return True
  else:
    print(f"{Fore.RED}FAIL     {Fore.RESET}({str(duration).rjust(3)}ms) - expected {expected_code}, got {response.status_code}")
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

  APP_NAME = f"{IMAGE_NAME}--{USER_NAME}"

  def startApp(app_name): subprocess.run(f"docker start {app_name}", shell=True, capture_output=True)
  def killApp(app_name): subprocess.run(f"docker kill {app_name}", shell=True, capture_output=True)
  def removeImage(image): subprocess.run(f"docker rmi {image}", shell=True, capture_output=True)
  def createApp(image, user): subprocess.run(f"docker create --name {image}.{user} {image}", shell=True, capture_output=True)
  def deleteApp(app_name): subprocess.run(f"docker rm {app_name}", shell=True, capture_output=True)

  print("\nStarting testing...")
  start_time = datetime.now()

  print()
  test("Create app - success",                           "POST", f"{BASE_URL}/{FACILITY_ID}/swarm-create-app?image={IMAGE_NAME}&user={USER_NAME}", 200)
  test("Create app - app already exists",                "POST", f"{BASE_URL}/{FACILITY_ID}/swarm-create-app?image={IMAGE_NAME}&user={USER_NAME}", 400)
  test("Create app - invalid facility ID",               "POST", f"{BASE_URL}/iaminvalid/swarm-create-app?image={IMAGE_NAME}&user={USER_NAME}", 400)
  test("Create app - invalid image name",                "POST", f"{BASE_URL}/{FACILITY_ID}/swarm-create-app?image=iaminvalid&user={USER_NAME}", 400)
  test("Create app - no image name",                     "POST", f"{BASE_URL}/{FACILITY_ID}/swarm-create-app?user={USER_NAME}", 400)
  test("Create app - no user name",                      "POST", f"{BASE_URL}/{FACILITY_ID}/swarm-create-app?image={IMAGE_NAME}", 400)
  
  print()
  test("Kill container - success",                       "POST", f"{BASE_URL}/{FACILITY_ID}/swarm-kill-app?name={APP_NAME}", 200)
  test("Kill container - invalid facility ID",           "POST", f"{BASE_URL}/iaminvalid/swarm-kill-app?name={APP_NAME}", 400)
  test("Kill container - invalid app name",              "POST", f"{BASE_URL}/{FACILITY_ID}/swarm-kill-app?name=iaminvalid", 400)
  test("Kill container - no app name",                   "POST", f"{BASE_URL}/{FACILITY_ID}/swarm-kill-app", 400)
  #startApp(APP_NAME)

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
