import flask
import subprocess
import os
import json


def getContainerID(app_name:str):
  """
  this helper function that returns the id of the container matching the given name
  Returns None if unsuccessful
  """

  # executing system command
  completedResponse = subprocessRun(f"docker ps -a --filter name={app_name} --format \"{{{{.Names}}}} {{{{.ID}}}}\"", shell=True, capture_output=True)
  if completedResponse.returncode != 0: return None
  if completedResponse.stdout == b'': return None

  # make list of names and ids
  nameList = [tuple(line.split()) for line in completedResponse.stdout.decode().split("\n") if line != ""]

  # check if app_name is in list
  for name, id in nameList:
    if name == app_name:
      return id

  return None


def getServiceID(app_name:str):
  """
  this helper function that returns the id of the service matching the given name
  Returns None if unsuccessful
  """

  # executing system command
  completedResponse = subprocessRun(f"docker service ls --filter name={app_name} --format \"{{{{.Name}}}} {{{{.ID}}}}\"", shell=True, capture_output=True)
  if completedResponse.returncode != 0: return None
  if completedResponse.stdout == b'': return None

  # make list of names and ids
  nameList = [tuple(line.split()) for line in completedResponse.stdout.decode().split("\n") if line != ""]

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
        return flask.make_response("Invalid facility ID", 400)
    elif "facility_id" not in kwargs.keys():
      if args[0] != "demo":
        return flask.make_response("Invalid facility ID", 400)

    return function(*args, **kwargs)

  decoratorFunction.__name__ = function.__name__
  return decoratorFunction



def verifyDockerEngine(swarm_method: bool):
  def decorator(function):
    """
    this decorator verifies that docker engine is running and responsive
    """
    def decoratorFunction(*args, **kwargs):

      completedResponse = subprocessRun("docker info --format json", shell=True, capture_output=True)
      if completedResponse.returncode != 0:
        return flask.make_response("Docker daemon not responding", 500)
      
      if swarm_method == (json.loads(completedResponse.stdout.decode())["Swarm"]["LocalNodeState"] == "active"):
        return function(*args, **kwargs)
      
      if swarm_method:
        return flask.make_response("Cannot use swarm method on non-swarm node", 400)
      else:
        return flask.make_response("Cannot use non-swarm method on swarm node", 400)

    decoratorFunction.__name__ = function.__name__
    return decoratorFunction
  return decorator


def handleAppName(function):
  """
  this decorator verifies that the given function received an app name argument,
  and that the container given is on the machine.
  """
  def decoratorFunction(*args, **kwargs):

    app_name = flask.request.args.get("name")
    if app_name == None:
      return flask.make_response("No container name provided", 400)

    app_names = app_name.split(",")

    if len(app_names) == 1:
      app_id = getContainerID(app_name)
      if app_id == None:
        return flask.make_response(f"Unable to find app \"{app_name}\"", 400)

      kwargs["app_name"] = app_name
      kwargs["app_id"] = app_id

      return function(*args, **kwargs)
    else: # batch methods
      successes = 0
      total = 0
      for app_name in app_names:
        print("app:", app_name)
        if app_name == "":
          continue

        total += 1
        app_id = getContainerID(app_name)
        if app_id == None:
          continue

        kwargs["app_name"] = app_name
        kwargs["app_id"] = app_id

        response = function(*args, **kwargs)
        if response.status_code == 200:
          successes += 1

      return flask.make_response(f"{successes}/{total} succeeded", 200 if successes == total else 400)

  decoratorFunction.__name__ = function.__name__
  return decoratorFunction


def handleSwarmAppName(function):
  """
  this decorator verifies that the given function received an app name argument,
  and that the container given is on the machine.
  """
  def decoratorFunction(*args, **kwargs):

    app_name = flask.request.args.get("name")
    if app_name == None:
      return flask.make_response("No container name provided", 400)

    app_names = app_name.split(",")

    if len(app_names) == 1:
      app_id = getServiceID(app_name)
      if app_id == None:
        return flask.make_response(f"Unable to find app \"{app_name}\"", 400)

      kwargs["app_name"] = app_name
      kwargs["app_id"] = app_id

      return function(*args, **kwargs)
    else: # batch methods
      successes = 0
      total = 0
      for app_name in app_names:
        print("app:", app_name)
        if app_name == "":
          continue

        total += 1
        app_id = getServiceID(app_name)
        if app_id == None:
          continue

        kwargs["app_name"] = app_name
        kwargs["app_id"] = app_id

        response = function(*args, **kwargs)
        if response.status_code == 200:
          successes += 1

      return flask.make_response(f"{successes}/{total} succeeded", 200 if successes == total else 400)

  decoratorFunction.__name__ = function.__name__
  return decoratorFunction


def subprocessRun(cmd_str: str, capture_output=True, shell=True) -> subprocess.CompletedProcess:
  """
  This wrapper function adds sudo in front of docker commands on unix systems
  """
  if not os.name == "nt":
    cmd_str = "sudo " + cmd_str
  return subprocess.run(cmd_str, capture_output=capture_output, shell=shell)