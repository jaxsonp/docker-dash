import json
import flask
from subprocess import TimeoutExpired
from methods import internal_methods

@internal_methods.verifyServerID
@internal_methods.verifyDockerEngine(swarm_method=True)
def swarmGetAppStats(server_id, app_name="", app_id="") -> flask.Response:
  """
  Returns hardware and resource stats of the specified app, or all apps if no name is provided.

  parameters:
    server_id - this value is passed in the API route, for demo purposes this should always be "demo"
    app_name (optional) - this value is passed as an http parameter

  returns:
    if successful, returns app stats in json format
  """

  app_name = flask.request.args.get("name")

  #get local hostname
  completedProcess = internal_methods.subprocessRun("hostname")
  local_hostname = completedProcess.stdout.decode().strip()

  # get all app stats
  if app_name == None:
    
    # get list of all node hostnames
    completedProcess = internal_methods.subprocessRun("docker node ls --format {{.Hostname}}")
    if completedProcess.returncode != 0:
      return flask.make_response(f"Uncaught error:\n"+completedProcess.stdout.decode()+"\n"+completedProcess.stderr.decode(), 500)
    hostname_list = [name for name in completedProcess.stdout.decode().split("\n") if name != ""]

    # add all containers in each node to output_list
    output_list = []
    for hostname in hostname_list:

      if hostname == local_hostname:

        # get stats of local containers
        completedProcess = internal_methods.subprocessRun("docker stats -a --no-stream --format json")
        if completedProcess.returncode != 0:
          return flask.make_response(f"Uncaught error:\n"+completedProcess.stdout.decode()+"\n"+completedProcess.stderr.decode(), 500)

        # add all containers to output_list
        for app in completedProcess.stdout.decode().strip().split("\n"):
          output_list.append(json.loads(app))
        
      else:

        # get username and ip address of node in question
        completedProcess = internal_methods.subprocessRun(f"docker node inspect --format json {hostname}")
        if completedProcess.returncode != 0:
          return flask.make_response(f"Uncaught error:\n"+completedProcess.stdout.decode()+"\n"+completedProcess.stderr.decode(), 500)
        node = json.loads(completedProcess.stdout.decode())[0]
        if not "Labels" in node["Spec"] or not "username" in node["Spec"]["Labels"]:
          return flask.make_response("Cannot find node username (make sure all nodes have the label 'username' which is the current user's name)", 500)
        node_username = node["Spec"]["Labels"]["username"]
        node_ip = node["Status"]["Addr"]

        # ssh into node and get stats of local containers
        try:
          completedProcess = internal_methods.subprocessRun(f"ssh {node_username}@{node_ip} docker stats -a --no-stream --format json", timeout=5)
        except TimeoutExpired:
          return flask.make_response(f"Cannot ssh into node '{hostname}' (make sure this node has the shared ssh key)", 500)
        if completedProcess.returncode != 0:
          return flask.make_response(f"Uncaught error:\n"+completedProcess.stdout.decode()+"\n"+completedProcess.stderr.decode(), 500)
        
        # add all containers to output_list
        for app in completedProcess.stdout.decode().strip().split("\n"):
          if app == "": continue
          output_list.append(json.loads(app))
    
    return flask.make_response(json.dumps(output_list), 200)


  # get specific app stats
  else:

    # check that app exists
    app_id = internal_methods.getContainerID(app_name)
    if app_id == None:
      return flask.make_response(f"Unable to find app \"{app_name}\"", 400)
    
    # get hostname of node that service is running on
    completedProcess = internal_methods.subprocessRun(f"docker service ps -f desired-state=complete --format json {app_name}")
    if completedProcess.returncode != 0:
      return flask.make_response(f"Uncaught error:\n"+completedProcess.stdout.decode()+"\n"+completedProcess.stderr.decode(), 500)
    app_list = [name for name in completedProcess.stdout.decode().strip().split("\n") if name != ""]
    app_list = list(map(json.loads, app_list))
    app_hostname = app_list[0]["Node"]

    # if app is running on the current node
    if app_hostname == local_hostname:

      # get stats of local containers
      completedProcess = internal_methods.subprocessRun("docker stats -a --no-stream --format json")
      if completedProcess.returncode != 0:
        return flask.make_response(f"Uncaught error:\n"+completedProcess.stdout.decode()+"\n"+completedProcess.stderr.decode(), 500)

      # find the correct container
      output_list = completedProcess.stdout.decode().strip().split("\n")
      output_list = list(map(json.loads, output_list))
      for entry in output_list:
        if entry["Name"].split(".")[0] == app_name:
          return flask.make_response(json.dumps(entry), 200)
      
      return flask.make_response("Something went wrong", 500)

    # app is running on a worker node
    else:

      # get username and ip address of node in question
      completedProcess = internal_methods.subprocessRun(f"docker node inspect --format json {app_hostname}")
      if completedProcess.returncode != 0:
        return flask.make_response(f"Uncaught error:\n"+completedProcess.stdout.decode()+"\n"+completedProcess.stderr.decode(), 500)
      node = json.loads(completedProcess.stdout.decode())[0]
      if not "Labels" in node["Spec"] or not "username" in node["Spec"]["Labels"]:
        return flask.make_response("Cannot find node username (make sure all nodes have the label 'username' which is the current user's name)", 500)
      node_username = node["Spec"]["Labels"]["username"]
      node_ip = node["Status"]["Addr"]

      # ssh into node and get stats of local containers
      try:
        completedProcess = internal_methods.subprocessRun(f"ssh {node_username}@{node_ip} docker stats -a --no-stream --format json", timeout=5)
      except TimeoutExpired:
        return flask.make_response(f"Cannot ssh into node '{app_hostname}' (make sure this node has an authorized ssh key)", 500)
      if completedProcess.returncode != 0:
        return flask.make_response(f"Uncaught error:\n"+completedProcess.stdout.decode()+"\n"+completedProcess.stderr.decode(), 500)

      # find the correct container
      output_list = completedProcess.stdout.decode().strip().split("\n")
      output_list = list(map(json.loads, output_list))
      for entry in output_list:
        if entry["Name"].split(".")[0] == app_name:
          return flask.make_response(json.dumps(entry), 200)
      
      return flask.make_response("Something went wrong", 500)