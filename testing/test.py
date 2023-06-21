from requests import get, post
from colorama import Fore, Style
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
        print(Fore.GREEN + "SUCCESS", Fore.RESET)
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

    print("\nStarting testing...")
    startTime = datetime.now()
    total = 39
    successful = 0

    killApp()
    print()
    if test("Start container - success",                    "POST", f"{BASE_URL}/{FACILITY_ID}/startApp?name={APP_NAME}",    200): successful += 1
    if test("Start container - invalid facility ID",        "POST", f"{BASE_URL}/iaminvalid/startApp?name={APP_NAME}",       400): successful += 1
    if test("Start container - invalid app name",           "POST", f"{BASE_URL}/{FACILITY_ID}/startApp?name=iaminvalid",    400): successful += 1
    if test("Start container - no app name",                "POST", f"{BASE_URL}/{FACILITY_ID}/startApp",                         400): successful += 1
    
    print()
    if test("Stop container - success",                     "POST", f"{BASE_URL}/{FACILITY_ID}/stopApp?name={APP_NAME}",     200): successful += 1
    if test("Stop container - invalid facility ID",         "POST", f"{BASE_URL}/iaminvalid/stopApp?name={APP_NAME}",        400): successful += 1
    if test("Stop container - invalid app name",            "POST", f"{BASE_URL}/{FACILITY_ID}/stopApp?name=iaminvalid",     400): successful += 1
    if test("Stop container - no app name",                 "POST", f"{BASE_URL}/{FACILITY_ID}/stopApp",                          400): successful += 1
    startApp()

    print()
    if test("Pause container - success",                    "POST", f"{BASE_URL}/{FACILITY_ID}/pauseApp?name={APP_NAME}",    200): successful += 1
    if test("Pause container - invalid facility ID",        "POST", f"{BASE_URL}/iaminvalid/pauseApp?name={APP_NAME}",       400): successful += 1
    if test("Pause container - invalid app name",           "POST", f"{BASE_URL}/{FACILITY_ID}/pauseApp?name=iaminvalid",    400): successful += 1
    if test("Pause container - no app name",                "POST", f"{BASE_URL}/{FACILITY_ID}/pauseApp",                         400): successful += 1
    
    print()
    if test("Unpause container - success",                  "POST", f"{BASE_URL}/{FACILITY_ID}/unpauseApp?name={APP_NAME}",  200): successful += 1
    if test("Unpause container - invalid facility ID",      "POST", f"{BASE_URL}/iaminvalid/unpauseApp?name={APP_NAME}",     400): successful += 1
    if test("Unpause container - invalid app name",         "POST", f"{BASE_URL}/{FACILITY_ID}/unpauseApp?name=iaminvalid",  400): successful += 1
    if test("Unpause container - no app name",              "POST", f"{BASE_URL}/{FACILITY_ID}/unpauseApp",                       400): successful += 1

    print()
    if test("Restart container - success",                  "POST", f"{BASE_URL}/{FACILITY_ID}/restartApp?name={APP_NAME}",  200): successful += 1
    if test("Restart container - invalid facility ID",      "POST", f"{BASE_URL}/iaminvalid/restartApp?name={APP_NAME}",     400): successful += 1
    if test("Restart container - invalid app name",         "POST", f"{BASE_URL}/{FACILITY_ID}/restartApp?name=iaminvalid",  400): successful += 1
    if test("Restart container - no app name",              "POST", f"{BASE_URL}/{FACILITY_ID}/restartApp",                       400): successful += 1
    
    print()
    if test("Kill container - success",                     "POST", f"{BASE_URL}/{FACILITY_ID}/killApp?name={APP_NAME}",     200): successful += 1
    if test("Kill container - invalid facility ID",         "POST", f"{BASE_URL}/iaminvalid/killApp?name={APP_NAME}",        400): successful += 1
    if test("Kill container - invalid app name",            "POST", f"{BASE_URL}/{FACILITY_ID}/killApp?name=iaminvalid",     400): successful += 1
    if test("Kill container - no app name",                 "POST", f"{BASE_URL}/{FACILITY_ID}/killApp",                          400): successful += 1
    startApp()

    print()
    if test("Get container names - success",                "GET", f"{BASE_URL}/{FACILITY_ID}/getAppNames",                           200): successful += 1
    if test("Get container names - invalid facility ID",    "GET", f"{BASE_URL}/iaminvalid/getAppNames",                              400): successful += 1
    
    print()
    if test("Get container status - success",               "GET", f"{BASE_URL}/{FACILITY_ID}/getAppStatus?name={APP_NAME}",        200): successful += 1
    if test("Get container status - invalid facility ID",   "GET", f"{BASE_URL}/iaminvalid/getAppStatus?name={APP_NAME}",           400): successful += 1
    if test("Get container status - invalid app name",      "GET", f"{BASE_URL}/{FACILITY_ID}/getAppStatus?name=iaminvalid",        400): successful += 1
    if test("Get container status - no app name",           "GET", f"{BASE_URL}/{FACILITY_ID}/getAppStatus",                             400): successful += 1

    print()
    if test("Get container info - success",                 "GET", f"{BASE_URL}/{FACILITY_ID}/getAppInfo?name={APP_NAME}",   200): successful += 1
    if test("Get container info - invalid facility ID",     "GET", f"{BASE_URL}/iaminvalid/getAppInfo?name={APP_NAME}",      400): successful += 1
    if test("Get container info - invalid app name",        "GET", f"{BASE_URL}/{FACILITY_ID}/getAppInfo?name=iaminvalid",   400): successful += 1
    if test("Get container info - no app name",             "GET", f"{BASE_URL}/{FACILITY_ID}/getAppInfo",                        400): successful += 1

    print()
    if test("Get health summary - success",                 "GET", f"{BASE_URL}/{FACILITY_ID}/getHealthSummary?name={APP_NAME}&duration=day", 200): successful += 1
    if test("Get health summary - invalid facility ID",     "GET", f"{BASE_URL}/iaminvalid/getHealthSummary?name={APP_NAME}&duration=day",    400): successful += 1
    if test("Get health summary - invalid app name",        "GET", f"{BASE_URL}/{FACILITY_ID}/getHealthSummary?name=iaminvalid&duration=day", 400): successful += 1
    if test("Get health summary - invalid duration",        "GET", f"{BASE_URL}/{FACILITY_ID}/getHealthSummary?name={APP_NAME}&duration=bad", 400): successful += 1
    if test("Get health summary - no duration",             "GET", f"{BASE_URL}/{FACILITY_ID}/getHealthSummary?name={APP_NAME}",              400): successful += 1

    testDuration = datetime.now() - startTime
    print(f"\n\nCompleted testing, {successful}/{total} tests successful (took {round(testDuration.total_seconds(), 2)} seconds)")
