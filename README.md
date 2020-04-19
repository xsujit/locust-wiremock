# Locust performance test against wire mock instance
Use following command to run the test
locust -f src/test/locust_test.py --no-web -c 1 -r 1 --run-time 1m
locust -f src/test/locust_test.py --csv=example --no-web -c 1 -r 1 --run-time 1m
locust -f src/test/locust_test.py --csv=example --no-web -c 10 -r 1 --run-time 2m --step-load --step-clients 5 --step-time 1m
