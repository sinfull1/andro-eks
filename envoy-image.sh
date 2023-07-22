#!/usr/bin sh

docker build -t envoy .
docker tag envoy 395283154402.dkr.ecr.ap-south-1.amazonaws.com/andromeda:envoy-13
docker push 395283154402.dkr.ecr.ap-south-1.amazonaws.com/andromeda:envoy-13