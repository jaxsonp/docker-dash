import flask
import subprocess
import json


def getContainerID(app_name:str):
  """
  this helper function that returns the id of the container matching the given name
  Returns None if unsuccessful
  """

  # checking if its in swarm mode
  completedProcess = None
  if checkSwarmMode():
    completedProcess = subprocessRun(f"docker service ls --filter name={app_name} --format \"{{{{.Name}}}} {{{{.ID}}}}\"")
  else:
    completedProcess = subprocessRun(f"docker ps -a --filter name={app_name} --format \"{{{{.Names}}}} {{{{.ID}}}}\"")
  if completedProcess.returncode != 0: return None
  if completedProcess.stdout == b'': return None

  # make list of names and ids
  nameList = [tuple(line.split()) for line in completedProcess.stdout.decode().split("\n") if line != ""]

  # check if app_name is in list
  for name, id in nameList:
    if name == app_name:
      return id

  return None


def checkSwarmMode() -> bool:
  """
  This helper function returns True if current node has swarm mode active, and False if not
  """
  completedProcess = subprocessRun("docker info --format json")
  return json.loads(completedProcess.stdout.decode())["Swarm"]["LocalNodeState"] == "active"

def subprocessRun(cmd_str: str, capture_output=True, shell=True, timeout=None) -> subprocess.CompletedProcess:
  """
  Wrapper for subprocess.run
  """

  return subprocess.run(cmd_str, capture_output=capture_output, shell=shell, timeout=timeout)


def verifyServerID(function):
  """
  this decorator verifies that the server id matches the expected input. For demo
  purposes, the id must match the string "demo".
  """
  def decoratorFunction(*args, **kwargs):
    #print("args:", args)
    #print("kwargs:", kwargs)

    # this is temporary just for the demo
    if "server_id" in kwargs.keys() and kwargs["server_id"] != "demo":
      if kwargs["server_id"] != "demo":
        return flask.make_response("Invalid server ID", 400)
    elif "server_id" not in kwargs.keys():
      if args[0] != "demo":
        return flask.make_response("Invalid server ID", 400)

    return function(*args, **kwargs)

  decoratorFunction.__name__ = function.__name__
  return decoratorFunction


def verifyDockerEngine(swarm_method=None):
  def decorator(function):
    """
    this decorator verifies that docker engine is running and responsive, and also checks that
    you aren't using a swarm function on a non-swarm mode and vice versa

    - swarm_method: True or False if a method is exclusively a swarm method or not a swarm method
        respectively, or None if it is swarm agnostic
    """
    def decoratorFunction(*args, **kwargs):

      completedProcess = subprocessRun("docker ps")
      if completedProcess.returncode != 0:
        return flask.make_response("Docker daemon not responding", 500)
      
      # checking swarm mode
      completedProcess = subprocessRun("docker info --format json")
      if swarm_method != None:
        if swarm_method == (json.loads(completedProcess.stdout.decode())["Swarm"]["LocalNodeState"] == "active"):
          return function(*args, **kwargs)
        
        if swarm_method:
          return flask.make_response("Cannot use swarm method on non-swarm node", 400)
        else:
          return flask.make_response("Cannot use non-swarm method on swarm node", 400)
      else:
        return function(*args, **kwargs)

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
      # non-batch calls
      app_id = getContainerID(app_name)
      if app_id == None:
        return flask.make_response(f"Unable to find app \"{app_name}\"", 400)

      kwargs["app_name"] = app_name
      kwargs["app_id"] = app_id

      return function(*args, **kwargs)
    else:
      # handling batch calls 
      successes = 0
      total = 0
      for app_name in app_names:
        #print("app:", app_name)
        if app_name == "":
          continue

        total += 1
        app_id = getContainerID(app_name)
        if app_id == None:
          continue

        kwargs["app_name"] = app_name
        kwargs["app_id"] = app_id

        # running the functions
        response = function(*args, **kwargs)
        if response.status_code == 200:
          successes += 1

      return flask.make_response(f"{successes}/{total} succeeded", 200 if successes == total else 400)

  decoratorFunction.__name__ = function.__name__
  return decoratorFunction