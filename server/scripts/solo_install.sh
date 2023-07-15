#!/bin/bash

echo -e "\n  > Starting install..."


# verifying sudo
sudo true

echo -n "  > Updating packages... "
sudo yum update -y
echo done

# start in home directory
cd ~
path="docker-dash"


# checking if dir exists
if [ -d "$path/" ]; then
  # prompting yes or no for overwrite
  while true; do
    read -p "Directory \"$path/\" already exists, overwrite? (y/n) " yn
    case $yn in 
      [yY] ) 
        break
        ;;
      [nN] ) 
        echo "  > Exiting..."; exit
        ;;
      * ) 
        echo invalid response
        ;;
    esac
  done
fi


# downloading github repo
echo -n "  > Downloading repository... "
curl -sSLo ./docker-dash.tar https://api.github.com/repos/JaxsonP/docker-dash/tarball
echo done

# extracting tar archive
echo -n "  > Extracting... "
sudo rm -rf "$path/"
mkdir "$path/"
tar -sxf ./docker-dash.tar -C ./$path/ --strip-components=1 &> /dev/null
sudo rm docker-dash.tar
echo done


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
        echo invalid response
        ;;
    esac
  done

  # installing docker
  echo -n "  > Installing docker... "
  sudo yum install -y yum-utils &> /dev/null
  sudo yum-config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo &> /dev/null
  sudo yum install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin &> /dev/null
fi
echo done

# configuring docker
echo -n "  > Configuring docker... "
sudo systemctl start docker
sudo systemctl enable docker &> /dev/null
sudo usermod -aG docker $USER
echo done

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
        echo Exiting...; exit
        ;;
      * ) 
        echo invalid response
        ;;
    esac
  done

  # installing python
  echo -n "  > Installing python (this may take a few minutes)... "
  sudo yum install -y make gcc openssl-devel bzip2-devel libffi-devel zlib-devel &> /dev/null
  curl -sOL https://www.python.org/ftp/python/3.9.16/Python-3.9.16.tgz &> /dev/null
  tar -xzf Python-3.9.16.tgz &> /dev/null
  cd Python-3.9.16 
  sudo ./configure --enable-optimizations &> /dev/null
  sudo make altinstall &> /dev/null
  cd ..
  sudo rm Python-3.9.16.tgz
  sudo rm -rf Python-3.9.16
fi
echo done

# installing and configing cron
echo -n "  > Configuring cron tabs... "
sudo yum install -y crontabs &> dev/null
sudo systemctl start crond.service
sudo systemctl enable crond.service
echo done

echo -e "\n  > To complete installation, a restart is required"
# prompting yes or no for restart
while true; do
  read -p "Do you want to restart now? (y/n) " yn
  case $yn in 
    [yY] ) 
      sudo shutdown -r now; exit
      ;;
    [nN] ) 
      echo Exiting...; exit
      ;;
    * ) 
      echo invalid response
      ;;
  esac
done
