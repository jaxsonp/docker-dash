#!/bin/bash

# node.csv format:
# ip,username,password

echo -e "\n  > Starting install"

# verifying sudo
sudo true


# checking if repo dir already exists
if [ -d "src-container-api/" ]; then
  # prompting yes or no for overwrite
  while true; do
    read -p "Directory \"src-container-api/\" already exists and will be overwritten, continue? (y/n) " yn
    case $yn in 
      [yY] ) 
        break
        ;;
      [nN] ) 
        echo "  > Exiting..."; exit
        ;;
      * ) 
        echo "Invalid response"
        ;;
    esac
  done
fi


# downloading github repo
echo -n "  > Downloading repository... "
curl -sSLo ./src-container-api.tar https://api.github.com/repos/JaxsonP/src-container-api/tarball
echo "done"


# extracting tar archive
echo -n "  > Extracting... "
sudo rm -rf src-container-api/
mkdir src-container-api/
tar -sxf ./src-container-api.tar -C ./src-container-api/ --strip-components=1 &> /dev/null
sudo rm src-container-api.tar
echo "done"

cd src-container-api


# query number of worker nodes
while true; do
  read -p "How many worker nodes will be added? " numWorkers
  if [[ $numWorkers =~ ^[0-9]+$ ]] ; then
    break
  fi
done


# get node information
echo -n ""  > nodes.csv
for (( i = 1 ; i < $numWorkers+1 ; i++ )); do

  # prompt for node ip address
  while true; do
    read -p "IP address of worker #$i: " ip
    if [[ ! -z "$ip" ]]; then
      break
    fi
  done
  # prompt for node username
  while true; do
    read -p "Username of worker #$i: " username
    if [[ ! -z "$username" ]]; then
      break
    fi
  done
  # prompt for node password
  while true; do
    read -s -p "Password of worker #$i: " password
    if [[ ! -z "$password" ]]; then
      break
    fi
  done
  echo ""
  echo "$ip,$username,$password" >> nodes.csv
done


# configuring ssh
echo -n "  > Configuring ssh... "
# generate key
keypath="/home/$USER/.ssh/id_srccontainerapi"
rm -f "$keypath" &> /dev/null
rm -f "$keypath.pub" &> /dev/null
ssh-keygen -b 2048 -f "$keypath" -N "" &> /dev/null
# copy key to workers
while IFS=, read -u 10 -r ip username password
do
  ./scripts/ssh_authorize "$username@$ip" "$keypath.pub" "$password" &> /dev/null
done 10< nodes.csv
sudo rm -f nodes.csv
echo "done"


# checking for docker
echo -n "  > Verifying docker... "
sudo docker ps &> /dev/null
if [ $? -gt 0 ]; then
  echo "not found"
  # prompting yes or no for docker installation
  while true; do
    read -p "Do you want to install Docker? (y/n) " yn
    case $yn in 
      [yY] ) 
        break
        ;;
      [nN] ) 
        echo Exiting...; exit
        ;;
      * ) 
        echo "Invalid response"
        ;;
    esac
  done

  # installing docker
  echo -n "  > Installing docker... "
  sudo yum install -y yum-utils &> /dev/null
  sudo yum-config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo &> /dev/null
  sudo yum install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin &> /dev/null
fi
echo "done"


# configuring docker
echo -n "  > Configuring docker... "
sudo systemctl start docker
sudo systemctl enable docker &> /dev/null
sudo usermod -aG docker $USER
echo "done"


# verifying python
echo -n "  > Verifying python... "
if [ "$(python3.9 --version 2>&1)" != "Python 3.9.16" ]; then
  echo "not found"
  # prompting yes or no for python installation
  while true; do
    read -p "Do you want to install Python 3.9.16? (y/n) " yn
    case $yn in 
      [yY] ) 
        break
        ;;
      [nN] ) 
        echo "  > Exiting..."; exit
        ;;
      * ) 
        echo "Invalid response"
        ;;
    esac
  done

  # installing python
  echo -n "  > Installing python (this may take a few minutes)... "
  sudo yum install -y gcc openssl-devel bzip2-devel libffi-devel zlib-devel &> /dev/null
  curl -sOL https://www.python.org/ftp/python/3.9.16/Python-3.9.16.tgz &> /dev/null
  tar -xzf Python-3.9.16.tgz &> /dev/null
  cd Python-3.9.16 
  sudo ./configure --enable-optimizations &> /dev/null
  sudo make altinstall &> /dev/null
  cd ..
  sudo rm Python-3.9.16.tgz
  sudo rm -rf Python-3.9.16
fi
echo "done"


# create docker swarm
joinfile="join_command.txt"
echo -n "  > Creating Docker swarm... "
sudo docker swarm init &> /dev/null
jointoken=$(sudo docker swarm join-token worker)
echo -e "run this command on each worker node:\nbash <(curl -s https://raw.githubusercontent.com/JaxsonP/src-container-api/master/scripts/swarm_install_worker.sh) ${jointoken:89}" > $joinfile
echo "done"
echo "  > NOTE: run the command found at 'src-containers-api/$joinfile' to set up the worker nodes"


# prompt for restart
echo -e "  > To complete installation, a restart is required"
while true; do
  read -p "Do you want to restart now? (y/n) " yn
  case $yn in 
    [yY] ) 
      sudo shutdown -r now; exit
      ;;
    [nN] ) 
      echo "  > Exiting...\n"; exit
      ;;
    * ) 
      echo "Invalid response"
      ;;
  esac
done

exit

# prompt for node hostname
# while true; do
#   read -p "Hostname of worker #$i: " hostname
#   if [[ ! -z "$hostname" ]]; then
#     # check that hostname is unique
#     unique=true
#     while read -u 10 line; do
#       if grep -q -E "^($hostname),[^,]*,[^,]*,[^,]*\$" nodes.csv; then
#         unique=false
#         break
#       fi
#     done 10<nodes.csv
#     if $unique; then
#       break
#     fi
#     echo "Hostname must be unique!"
#   fi
# done
