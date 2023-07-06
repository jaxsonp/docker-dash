#!/bin/bash

# verifying sudo
sudo true

# downloading github repo
echo -n "Downloading repository... "
curl -sSLo ./src-container-api.tar https://api.github.com/repos/JaxsonP/src-container-api/tarball
echo done

# extracting tar archive
echo -n "Extracting... "
rm -rf src-container-api/
mkdir src-container-api/
tar -sxf ./src-container-api.tar -C ./src-container-api/ --strip-components=1 > /dev/null;
rm src-container-api.tar
echo done


# checking for docker
echo -n "Verifying docker... "
sudo docker ps > /dev/null 2>&1
if [ $? -gt 0 ]
then
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
  echo -n "Installing docker... "
  yum install -y yum-utils > /dev/null
  sudo yum-config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo > /dev/null
  sudo yum install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin > /dev/null
fi
echo done

# configuring docker
echo -n "Configuring docker... "
sudo systemctl start docker
sudo systemctl enable docker > /dev/null
sudo usermod -aG docker $USER
echo done

# verifying python
echo -n "Verifying python... "
if [ "$(python3.9 --version 2>&1)" != "Python 3.9.16" ]
then
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
  echo -n "Installing python (this may take a few minutes)... "
  sudo yum install -y gcc openssl-devel bzip2-devel libffi-devel zlib-devel > /dev/null
  curl -sOL https://www.python.org/ftp/python/3.9.16/Python-3.9.16.tgz > /dev/null
  tar -xzf Python-3.9.16.tgz > /dev/null
  cd Python-3.9.16 
  sudo ./configure --enable-optimizations > /dev/null
  sudo make altinstall > /dev/null
  cd ..
  rm Python-3.9.16.tgz
  rm -rf Python-3.9.16
fi
echo done

echo -e "\nTo complete installation, a restart is required"
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
