from flask import Response, request
import subprocess


def getContainerID(app_name:str) -> str | None:
  """
  this helper function that returns the id of the container matching the given name
  Returns None if unsuccessful
  """

  # executing system command
  completedResponse = subprocess.run(f"docker ps -a --filter name={app_name} --format \"{{{{.Names}}}} {{{{.ID}}}}\"", capture_output=True)
  if completedResponse.returncode != 0: return None

  if completedResponse.stdout == b'': return None

  # make list of names and ids
  nameList = [tuple(line.split()) for line in completedResponse.stdout.decode().split("\n")]

  # check if app_name is in list
  for name, id in nameList:
    if name == app_name:
      return id

  return None


def verifyFacilityID(function):
  """
  this decorator verifies that the facility id matches the expected input. For demo
  purposes, the id must match the string "demo".
  """
  def decoratorFunction(*args, **kwargs):
    #print("args:", args)
    #print("kwargs:", kwargs)

    # this is temporary just for the demo
    if "facility_id" in kwargs.keys() and kwargs["facility_id"] != "demo":
      if kwargs["facility_id"] != "demo":
        return Response("Invalid facility ID", status=400)
    elif "facility_id" not in kwargs.keys():
      if args[0] != "demo":
        return Response("Invalid facility ID", status=400)

    return function(*args, **kwargs)

  decoratorFunction.__name__ = function.__name__
  return decoratorFunction



def verifyDockerEngine(function):
  """
  this decorator verifies that docker engine is running and responsive
  """
  def decoratorFunction(*args, **kwargs):

    completedResponse = subprocess.run("docker ps", capture_output=True)
    if completedResponse.returncode != 0:
      return Response("Docker daemon not responding", status=500)

    return function(*args, **kwargs)

  decoratorFunction.__name__ = function.__name__
  return decoratorFunction



def verifyAppName(function):
  """
  this decorator verifies that the given function received an app name argument,
  and that the container given is on the machine
  """
  def decoratorFunction(*args, **kwargs):

    app_name = request.args.get("name")
    if app_name == None:
      return Response("No container name provided", status=400)

    app_id = getContainerID(app_name)
    if app_id == None:
      return Response(f"Unable to find app \"{app_name}\"", status=400)

    kwargs["app_name"] = app_name
    kwargs["app_id"] = app_id

    return function(*args, **kwargs)

  decoratorFunction.__name__ = function.__name__
  return decoratorFunction