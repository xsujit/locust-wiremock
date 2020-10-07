
# Prerequisite - Wiremock
Download wiremock standalone jar and run it
E.g. java -jar wiremock-standalone-2.27.2.jar
java -jar wiremock-standalone-2.27.2.jar --disable-request-logging --async-response-enabled false
java -jar wiremock-standalone-2.27.2.jar --disable-request-logging --async-response-enabled true
For https add --https-port 8443

# Locust (v1.2.3) performance test against wire mock instance
Use following command to run the test
locust -f locust_test.py  --headless -u 2 -r 2 --run-time 30s --stop-timeout 2
locust -f locust_test.py  --headless -u 10 -r 1 --run-time 30s --csv=example
The test will delete any existing wiremock mappings.
It will create new mappings and the run the tests against those endpoints 

# Remove all stopped containers and images
docker rm $(docker ps -a -q)
# This will remove all dangling images.
docker image prune

# Build
docker build -t locustio/locust:wm-locust .
# Run
docker run --network="host" locustio/locust:wm-locust -f /src/test/locust_test.py --headless -u 1 -r 1 -t 10m

# access container
docker exec -it bae8b1a08180 bash

# Other docker commands
docker run -p 8089:8089 --network="host" -v $PWD:/mnt/locust locustio/locust -f /mnt/locust/locust_test.py --headless -u 1 -r 1 -t 1m
