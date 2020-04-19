
# Prerequisite - Wiremock
Download wiremock standalone jar and run it
E.g. java -jar wiremock-jre8-standalone-2.26.3.jar --https-port 8443

# Locust (v0.14.5) performance test against wire mock instance
Use following command to run the test
locust -f src/test/locust_test.py --no-web -c 1 -r 1 --run-time 1m
OR 
locust -f src/test/locust_test.py --csv=example --no-web -c 1 -r 1 --run-time 1m