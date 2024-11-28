
#TODO: use my own address and port on prod

docker pull redis/redis-stack-server:latest
docker run -d --name redis-stack-server -p 6379:6379 redis/redis-stack-server:latest