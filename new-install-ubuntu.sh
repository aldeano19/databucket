# INSTALL DOCKER

echo "-----------"
echo "ECHO #1"
echo "-----------"

sudo apt-get remove docker docker-engine docker.io
sudo apt-get update
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
sudo add-apt-repository \
   "deb [arch=amd64] https://download.docker.com/linux/ubuntu \
   $(lsb_release -cs) \
   stable"

echo "-----------"
echo "ECHO #2"
echo "-----------"

sudo apt-get update

# TODO: This line will not install on itself, needs to be run manually.
sudo apt-get install docker-ce
sudo apt-get install docker-ce=17.06.0~ce-0~ubuntu
sudo docker run hello-world

echo "-----------"
echo "ECHO #3"
echo "-----------"

# INSTALL DOCKER-COMPOSE
sudo -i
curl -L https://github.com/docker/compose/releases/download/1.15.0/docker-compose-`uname -s`-`uname -m` > /usr/local/bin/docker-compose
chmod +x /usr/local/bin/docker-compose
docker-compose --version