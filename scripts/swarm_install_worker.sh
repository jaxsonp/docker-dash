#!/bin/bash

echo -e "\n  > Starting install (worker node)"


if [ $# -le 0 ]; then
  echo "Missing token argument"; exit
fi
if [ $# -eq 1 ]; then
  echo "Missing IP address argument"; exit
fi
token=$1
ip_addr=$2


# verifying sudo
sudo true


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
        echo "  > Exiting..."; exit
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


# joining swarm
echo -n "  > Joining swarm... "
sudo firewall-cmd --add-port=2377/tcp --permanent &> /dev/null
sudo firewall-cmd --reload &> /dev/null
sudo docker swarm join --token $token $ip_addr


# configure node
echo -n "  > Configuring node... "
sudo docker node update --label-add username=$USER self &> /dev/null
sudo docker node demote self &> /dev/null
echo "done"


echo "  > To complete installation, a restart is required"
# prompting yes or no for restart
while true; do
  read -p "Do you want to restart now? (y/n) " yn
  case $yn in 
    [yY] ) 
      sudo shutdown -r now; exit
      ;;
    [nN] ) 
      echo "  > Exiting..."; exit
      ;;
    * ) 
      echo "Invalid response"
      ;;
  esac
done
