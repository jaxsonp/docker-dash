import json
import flask
from methods import internal_methods

@internal_methods.verifyFacilityID
@internal_methods.verifyDockerEngine(swarm_method=True)
def swarmGetAppStatus(facility_id, app_name="", app_id="") -> flask.Response:
  
  """
  Returns basic information and status of the specified app, or all apps if no name is provided.

  parameters:
    facility_id - this value is passed in the API route, for demo purposes this should always be "demo"
    app_name (optional) - this value is passed as an http parameter

  returns:
    if successful, returns app information in json format
  """
  
  app_name = flask.request.args.get("name")

  # get local hostname
  completedProcess = internal_methods.subprocessRun("hostname")
  local_hostname = completedProcess.stdout.decode().strip()

  # get statuses of all apps
  if app_name == None:
    
    # get list of all node hostnames
    completedProcess = internal_methods.subprocessRun("docker node ls --format {{.Hostname}}")
    if completedProcess.returncode != 0:
      return flask.make_response(f"Unknown error:\n"+completedProcess.stdout.decode()+"\n"+completedProcess.stderr.decode(), 500)
    hostname_list = [name for name in completedProcess.stdout.decode().split("\n") if name != ""]

    # add all processes in each node to output_list
    output_list = []
    for hostname in hostname_list:

      if hostname == local_hostname:

        # get status of local containers
        completedProcess = internal_methods.subprocessRun("docker ps -a --format json")
        if completedProcess.returncode != 0:
          return flask.make_response(f"Unknown error:\n"+completedProcess.stdout.decode()+"\n"+completedProcess.stderr.decode(), 500)

        # add all statuses to list
        for app in completedProcess.stdout.decode().strip().split("\n"):
          if app == "": continue
          app_json = json.loads(app)
          app_json["Names"] = app_json["Names"].split(".")[0]
          output_list.append(app_json)
        
      else:

        # get username and ip address of node in question
        completedProcess = internal_methods.subprocessRun(f"docker node inspect --format json {hostname}")
        if completedProcess.returncode != 0:
          return flask.make_response(f"Unknown error:\n"+completedProcess.stdout.decode()+"\n"+completedProcess.stderr.decode(), 500)
        node = json.loads(completedProcess.stdout.decode())[0]
        if not "Labels" in node["Spec"] or not "username" in node["Spec"]["Labels"]:
          return flask.make_response("Cannot find node username (make sure all nodes have the label 'username' which is the current user's name)", 500)
        node_username = node["Spec"]["Labels"]["username"]
        node_ip = node["Status"]["Addr"]

        # ssh into node and get stats of local containers
        try:
          completedProcess = internal_methods.subprocessRun(f"ssh {node_username}@{node_ip} docker ps -a --format json", timeout=5)
        except TimeoutExpired:
          return flask.make_response(f"Cannot ssh into node '{hostname}' (make sure this node has the shared ssh key)", 500)
        if completedProcess.returncode != 0:
          return flask.make_response(f"Unknown error:\n"+completedProcess.stdout.decode()+"\n"+completedProcess.stderr.decode(), 500)
        
        # add all containers to list
        for app in completedProcess.stdout.decode().strip().split("\n"):
          if app == "": continue
          app_json = json.loads(app)
          app_json["Names"] = app_json["Names"].split(".")[0]
          output_list.append(app_json)
    
    return flask.make_response(json.dumps(output_list), 200)

  # get status of specified app
  else:

    # check that app exists
    app_id = internal_methods.getContainerID(app_name)
    if app_id == None:
      return flask.make_response(f"Unable to find app \"{app_name}\"", 400)
    
    # get hostname of node that service is running on
    completedProcess = internal_methods.subprocessRun(f"docker service ps -f desired-state=complete --format json {app_name}")
    if completedProcess.returncode != 0:
      return flask.make_response(f"Unknown error:\n"+completedProcess.stdout.decode()+"\n"+completedProcess.stderr.decode(), 500)
    app_list = [name for name in completedProcess.stdout.decode().strip().split("\n") if name != ""]
    app_list = list(map(json.loads, app_list))
    app_hostname = app_list[0]["Node"]

    # if app is running on current node
    if app_hostname == local_hostname:

      # get stats of local containers
      completedProcess = internal_methods.subprocessRun("docker ps -a --format json")
      if completedProcess.returncode != 0:
        return flask.make_response(f"Unknown error:\n"+completedProcess.stdout.decode()+"\n"+completedProcess.stderr.decode(), 500)

      # find the correct container
      output_list = completedProcess.stdout.decode().strip().split("\n")
      output_list = list(map(json.loads, output_list))
      for entry in output_list:
        if entry["Names"].split(".")[0] == app_name:
          entry["Names"] = entry["Names"].split(".")[0]
          return flask.make_response(json.dumps(entry), 200)
      
      return flask.make_response("Something went wrong", 500)

    # app is running on a worker node
    else:

      # get username and ip address of node in question
      completedProcess = internal_methods.subprocessRun(f"docker node inspect --format json {app_hostname}")
      if completedProcess.returncode != 0:
        return flask.make_response(f"Unknown error:\n"+completedProcess.stdout.decode()+"\n"+completedProcess.stderr.decode(), 500)
      node = json.loads(completedProcess.stdout.decode())[0]
      if not "Labels" in node["Spec"] or not "username" in node["Spec"]["Labels"]:
        return flask.make_response("Cannot find node username (make sure all nodes have the label 'username' which is the current user's name)", 500)
      node_username = node["Spec"]["Labels"]["username"]
      node_ip = node["Status"]["Addr"]

      # ssh into node and get stats of local containers
      try:
        completedProcess = internal_methods.subprocessRun(f"ssh {node_username}@{node_ip} docker ps -a --format json", timeout=10)
      except TimeoutExpired:
        return flask.make_response(f"Cannot ssh into node '{app_hostname}' (make sure this node has an authorized ssh key)", 500)
      if completedProcess.returncode != 0:
        return flask.make_response(f"Unknown error:\n"+completedProcess.stdout.decode()+"\n"+completedProcess.stderr.decode(), 500)

      # find the correct container
      output_list = completedProcess.stdout.decode().strip().split("\n")
      output_list = list(map(json.loads, output_list))
      for entry in output_list:
        if entry["Names"].split(".")[0] == app_name:
          entry["Names"] = entry["Names"].split(".")[0]
          return flask.make_response(json.dumps(entry), 200)
      
      return flask.make_response("Something went wrong", 500)