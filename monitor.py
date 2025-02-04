# monitor.py - CI/CD Pipeline Health Monitor

import yaml
import re
import time
from prometheus_client import start_http_server, Gauge

# --- Configuration ---
def load_config(config_path='config.yaml'):
    """Loads configuration from YAML file."""
    with open(config_path, 'r') as file:
        return yaml.safe_load(file)

# --- Log Parsing ---
def parse_jenkins_log(log_path='sample_jenkins.log'):
    """Parses Jenkins log file and extracts relevant metrics."""
    test_times = {}
    failure_count = 0
    flaky_tests = {} # To be implemented

    with open(log_path, 'r') as file:
        for line in file:
            # Example log parsing - needs to be refined based on actual log format
            if "Finished: FAILURE" in line:
                failure_count += 1
            if "Testcase:" in line and "time=" in line:
                match = re.search(r"Testcase: (.+?) time=(.+?)s", line)
                if match:
                    test_name = match.group(1)
                    test_time = float(match.group(2))
                    test_times[test_name] = test_time
    return test_times, failure_count

# --- Prometheus Metrics ---
def initialize_metrics():
    """Initializes Prometheus metrics."""
    test_execution_gauge = Gauge('test_execution_time_seconds', 'Test execution time in seconds', ['test_name'])
    failure_count_gauge = Gauge('pipeline_failure_count', 'Number of pipeline failures')
    return test_execution_gauge, failure_count_gauge

def update_metrics(test_times, failure_count, test_execution_gauge, failure_count_gauge):
    """Updates Prometheus metrics with parsed data."""
    for test_name, test_time in test_times.items():
        test_execution_gauge.labels(test_name=test_name).set(test_time)
    failure_count_gauge.set(failure_count)

# --- Alerting ---
def check_thresholds_and_alert(config, test_times, failure_count):
    """Checks metrics against thresholds and sends alerts if necessary."""
    max_failure_threshold = config['thresholds']['max_failure_count']
    max_execution_time_threshold = config['thresholds']['max_test_execution_time']

    if failure_count > max_failure_threshold:
        send_alert(f"Failure count exceeded threshold: {failure_count} > {max_failure_threshold}")

    for test_name, test_time in test_times.items():
        if test_time > max_execution_time_threshold:
            send_alert(f"Test {test_name} execution time exceeded threshold: {test_time}s > {max_execution_time_threshold}s")

def send_alert(message):
    """Sends an alert - currently prints to console, to be extended to Slack/email."""
    print(f"ALERT: {message}")

# --- Main ---
def main():
    config = load_config()
    test_execution_gauge, failure_count_gauge = initialize_metrics()
    start_http_server(config['prometheus']['port']) # Expose metrics on specified port

    while True: # For periodic execution
        test_times, failure_count = parse_jenkins_log()
        update_metrics(test_times, failure_count, test_execution_gauge, failure_count_gauge)
        check_thresholds_and_alert(config, test_times, failure_count)
        print("Metrics updated and thresholds checked.") # Simple logging for demonstration
        time.sleep(config['monitor']['interval']) # Check interval from config

if __name__ == "__main__":
    main()
