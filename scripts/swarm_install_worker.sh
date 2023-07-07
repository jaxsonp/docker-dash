#!/bin/bash

index=$1

# checking for docker
echo -n "Verifying docker on worker #$index... "
sudo docker ps &> /dev/null
if [ $? -gt 0 ]; then
  echo "not found"

  # installing docker
  echo -n "Installing docker on worker #$index... "
  sudo yum install -y yum-utils &> /dev/null
  sudo yum-config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo &> /dev/null
  sudo yum install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin &> /dev/null
fi
echo done

# configuring docker
echo -n "Configuring docker on worker #$index... "
sudo systemctl start docker
sudo systemctl enable docker &> /dev/null
sudo usermod -aG docker $USER
echo done