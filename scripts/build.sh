source ./scripts/ambiente.sh

docker build \
-f ./dockerfile-bash \
--build-arg TAG=$VERSION \
-t $DOCKER_HUB_REPO/$DOCKER_HUB_GROUP/$PROYECTO:$VERSION .
