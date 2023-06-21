from requests import get, post
from datetime import datetime


def test(testname:str, method:str, url:str, expectedCode:int):
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
        print("SUCCESS")
        return True
    else:
        print(f"FAIL: expected {expectedCode}, got {response.status_code} ({response.text[:150]})")
        return False


if __name__ == "__main__":

    #read secrets.txt
    with open("testing/secrets.txt", "r") as f:
        lines = [tuple(line.split("=")) for line in f.readlines()]
    BASE_URL = lines[0][1].strip()
    FACILITY_ID = lines[1][1].strip()
    APP_NAME = lines[2][1].strip()

    def startContainer():
        post(f"{BASE_URL}/{FACILITY_ID}/startContainer?container={APP_NAME}")

    def killContainer():
        post(f"{BASE_URL}/{FACILITY_ID}/killContainer?container={APP_NAME}")

    print("\nStarting testing...")
    startTime = datetime.now()
    total = 39
    successful = 0

    killContainer()
    print()
    if test("Start container - success",                    "POST", f"{BASE_URL}/{FACILITY_ID}/startContainer?container={APP_NAME}",    200): successful += 1
    if test("Start container - invalid facility ID",        "POST", f"{BASE_URL}/iaminvalid/startContainer?container={APP_NAME}",       400): successful += 1
    if test("Start container - invalid app name",           "POST", f"{BASE_URL}/{FACILITY_ID}/startContainer?container=iaminvalid",    400): successful += 1
    if test("Start container - no app name",                "POST", f"{BASE_URL}/{FACILITY_ID}/startContainer",                         400): successful += 1
    
    print()
    if test("Stop container - success",                     "POST", f"{BASE_URL}/{FACILITY_ID}/stopContainer?container={APP_NAME}",     200): successful += 1
    if test("Stop container - invalid facility ID",         "POST", f"{BASE_URL}/iaminvalid/stopContainer?container={APP_NAME}",        400): successful += 1
    if test("Stop container - invalid app name",            "POST", f"{BASE_URL}/{FACILITY_ID}/stopContainer?container=iaminvalid",     400): successful += 1
    if test("Stop container - no app name",                 "POST", f"{BASE_URL}/{FACILITY_ID}/stopContainer",                          400): successful += 1
    startContainer()

    print()
    if test("Pause container - success",                    "POST", f"{BASE_URL}/{FACILITY_ID}/pauseContainer?container={APP_NAME}",    200): successful += 1
    if test("Pause container - invalid facility ID",        "POST", f"{BASE_URL}/iaminvalid/pauseContainer?container={APP_NAME}",       400): successful += 1
    if test("Pause container - invalid app name",           "POST", f"{BASE_URL}/{FACILITY_ID}/pauseContainer?container=iaminvalid",    400): successful += 1
    if test("Pause container - no app name",                "POST", f"{BASE_URL}/{FACILITY_ID}/pauseContainer",                         400): successful += 1
    
    print()
    if test("Unpause container - success",                  "POST", f"{BASE_URL}/{FACILITY_ID}/unpauseContainer?container={APP_NAME}",  200): successful += 1
    if test("Unpause container - invalid facility ID",      "POST", f"{BASE_URL}/iaminvalid/unpauseContainer?container={APP_NAME}",     400): successful += 1
    if test("Unpause container - invalid app name",         "POST", f"{BASE_URL}/{FACILITY_ID}/unpauseContainer?container=iaminvalid",  400): successful += 1
    if test("Unpause container - no app name",              "POST", f"{BASE_URL}/{FACILITY_ID}/unpauseContainer",                       400): successful += 1

    print()
    if test("Restart container - success",                  "POST", f"{BASE_URL}/{FACILITY_ID}/restartContainer?container={APP_NAME}",  200): successful += 1
    if test("Restart container - invalid facility ID",      "POST", f"{BASE_URL}/iaminvalid/restartContainer?container={APP_NAME}",     400): successful += 1
    if test("Restart container - invalid app name",         "POST", f"{BASE_URL}/{FACILITY_ID}/restartContainer?container=iaminvalid",  400): successful += 1
    if test("Restart container - no app name",              "POST", f"{BASE_URL}/{FACILITY_ID}/restartContainer",                       400): successful += 1
    
    print()
    if test("Kill container - success",                     "POST", f"{BASE_URL}/{FACILITY_ID}/killContainer?container={APP_NAME}",     200): successful += 1
    if test("Kill container - invalid facility ID",         "POST", f"{BASE_URL}/iaminvalid/killContainer?container={APP_NAME}",        400): successful += 1
    if test("Kill container - invalid app name",            "POST", f"{BASE_URL}/{FACILITY_ID}/killContainer?container=iaminvalid",     400): successful += 1
    if test("Kill container - no app name",                 "POST", f"{BASE_URL}/{FACILITY_ID}/killContainer",                          400): successful += 1
    startContainer()

    print()
    if test("Get container names - success",                "GET", f"{BASE_URL}/{FACILITY_ID}/getContainers",                           200): successful += 1
    if test("Get container names - invalid facility ID",    "GET", f"{BASE_URL}/iaminvalid/getContainers",                              400): successful += 1
    
    print()
    if test("Get container status - success",               "GET", f"{BASE_URL}/{FACILITY_ID}/queryStatus?container={APP_NAME}",        200): successful += 1
    if test("Get container status - invalid facility ID",   "GET", f"{BASE_URL}/iaminvalid/queryStatus?container={APP_NAME}",           400): successful += 1
    if test("Get container status - invalid app name",      "GET", f"{BASE_URL}/{FACILITY_ID}/queryStatus?container=iaminvalid",        400): successful += 1
    if test("Get container status - no app name",           "GET", f"{BASE_URL}/{FACILITY_ID}/queryStatus",                             400): successful += 1

    print()
    if test("Get container info - success",                 "GET", f"{BASE_URL}/{FACILITY_ID}/inspectContainer?container={APP_NAME}",   200): successful += 1
    if test("Get container info - invalid facility ID",     "GET", f"{BASE_URL}/iaminvalid/inspectContainer?container={APP_NAME}",      400): successful += 1
    if test("Get container info - invalid app name",        "GET", f"{BASE_URL}/{FACILITY_ID}/inspectContainer?container=iaminvalid",   400): successful += 1
    if test("Get container info - no app name",             "GET", f"{BASE_URL}/{FACILITY_ID}/inspectContainer",                        400): successful += 1

    print()
    if test("Get health summary - success",                 "GET", f"{BASE_URL}/{FACILITY_ID}/getHealthSummary?container={APP_NAME}&duration=day", 200): successful += 1
    if test("Get health summary - invalid facility ID",     "GET", f"{BASE_URL}/iaminvalid/getHealthSummary?container={APP_NAME}&duration=day",    400): successful += 1
    if test("Get health summary - invalid app name",        "GET", f"{BASE_URL}/{FACILITY_ID}/getHealthSummary?container=iaminvalid&duration=day", 400): successful += 1
    if test("Get health summary - invalid duration",        "GET", f"{BASE_URL}/{FACILITY_ID}/getHealthSummary?container={APP_NAME}&duration=bad", 400): successful += 1
    if test("Get health summary - no duration",             "GET", f"{BASE_URL}/{FACILITY_ID}/getHealthSummary?container={APP_NAME}",              400): successful += 1

    testDuration = datetime.now() - startTime
    print(f"\n\nCompleted testing, {successful}/{total} tests successful (took {round(testDuration.total_seconds(), 2)} seconds)")
