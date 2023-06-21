from flask import Response, request
import subprocess


def getContainerID(container_name:str) -> str | None:
  """
  this helper function that returns the id of the container matching the given name
  Returns None if unsuccessful
  """

  # executing system command
  completedResponse = subprocess.run(f"docker ps -a --filter name={container_name} --format \"{{{{.Names}}}} {{{{.ID}}}}\"", capture_output=True)
  if completedResponse.returncode != 0: return None

  if completedResponse.stdout == b'': return None

  # make list of names and ids
  nameList = [tuple(line.split()) for line in completedResponse.stdout.decode().split("\n")]

  # check if container_name is in list
  for name, id in nameList:
    if name == container_name:
      return id

  return None


def verifyFacilityID(function):
  """
  this decorator verifies that the facility id matches the expected input. For demo
  purposes, the id must match the string "demo".
  """
  def decoratorFunction(*args, **kwargs):

    # this is temporary just for the demo
    if kwargs["facility_id"] != "demo":
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

def verifyContainer(function):
  """
  this decorator verifies that the given function received a container argument,
  and that the container given is on the machine
  """
  def decoratorFunction(*args, **kwargs):

    container_name = request.args.get("container")
    if container_name == None:
      return Response("No container name provided", status=400)

    container_id = getContainerID(container_name)
    if container_id == None:
      return Response(f"Unable to find app \"{container_name}\"", status=400)

    kwargs["container_name"] = container_name
    kwargs["container_id"] = container_id

    return function(*args, **kwargs)

  decoratorFunction.__name__ = function.__name__
  return decoratorFunction