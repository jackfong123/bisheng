# sudo docker network create my-network
# bash run_redis.sh
# bash run_backend.sh
# qianwen：sk-a853352b89dd4ef198b1801ae99b16ec

CURPATH=$PWD
cd "$CURPATH/docker"
sudo docker-compose down
cd "$CURPATH"
sudo rm -rf docker/data/*
sudo rm -rf docker/mysql/data/*
cd "$CURPATH/docker"
sudo docker-compose up -d