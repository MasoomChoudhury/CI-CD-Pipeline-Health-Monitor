# CI/CD Pipeline Health Monitor 

## Overview

This project demonstrates a simple CI/CD pipeline health monitor built in Python. It parses Jenkins log files, extracts key metrics like test execution times and failure counts, and exposes these metrics via Prometheus for visualization in Grafana. It also includes basic alerting functionality.

**Key Features:**

- **Log Analysis:** Parses Jenkins log files to extract test execution times and failure counts.
- **Configuration:** Uses a `config.yaml` file to define thresholds for metrics and monitoring intervals.
- **Prometheus Integration:** Exposes metrics in Prometheus format on `/metrics` endpoint.
- **Basic Alerting:** Includes a function to check for threshold breaches and send alerts (currently prints to console).
- **Sample Data:** Includes a `sample_jenkins.log` file for testing.

## Getting Started

### Prerequisites

- Python 3.x
- pip (Python package installer)
- Prometheus client library: `pip install prometheus_client pyyaml`
- (Optional) Docker and Docker Compose for containerization

### Installation and Setup

1. **Clone the repository (if applicable):**

   ```bash
   git clone [repository-url]
   cd CI-CD-Pipeline-Health-Monitor
   ```

2. **Install Python dependencies:**

   ```bash
   pip install prometheus_client pyyaml
   ```

3. **Configuration:**

   - Modify `config.yaml` to adjust thresholds, Prometheus port, and monitoring interval as needed.

### Running the Monitor Locally

1. **Run the Python script:**

   ```bash
   python monitor.py
   ```

   This will start the monitor, which will:
     - Load configurations from `config.yaml`.
     - Initialize Prometheus metrics.
     - Start a Prometheus HTTP server on the port specified in `config.yaml` (default: 9090).
     - Periodically parse `sample_jenkins.log`, update metrics, and check for alerts based on the interval in `config.yaml` (default: 30 seconds).
     - Print alerts to the console if thresholds are breached.

2. **Access Prometheus Metrics:**

   - Open your browser and go to `http://localhost:9090/metrics` (or the port configured in `config.yaml`). You should see the Prometheus metrics exposed by the monitor.

### Setting up Prometheus and Grafana (Optional)

To visualize the metrics in Grafana, you need to set up Prometheus to scrape the metrics endpoint exposed by the monitor.

1. **Run Prometheus:**

   - Ensure you have Prometheus installed and configured.
   - Configure Prometheus to scrape the monitor's metrics endpoint (e.g., `http://localhost:9090/metrics`).  You can add a job to your `prometheus.yml` like this:

     ```yaml
     scrape_configs:
       - job_name: 'pipeline-monitor'
         scrape_interval: 30s
         static_configs:
           - targets: ['localhost:9090'] # Or the host and port where monitor.py is running
     ```
   - Start Prometheus.

2. **Run Grafana:**

   - Ensure you have Grafana installed and running.
   - Add Prometheus as a data source in Grafana, pointing to your Prometheus instance.
   - **Import Dashboard (Optional):** If a `dashboard.json` file is provided, you can import it into Grafana to get a pre-configured dashboard for visualizing the metrics.  (Instructions on importing dashboards in Grafana are available in the Grafana documentation).

### Alerting Configuration

- **Current Alerting:** The current implementation of alerting in `monitor.py` simply prints alert messages to the console.
- **Extending to Slack/Email:**
    - To integrate with Slack or email, you would need to:
        - Install necessary libraries (e.g., `slack_sdk` for Slack, `smtplib` and `email` for email).
        - Configure Slack webhook URL or email server settings in `config.yaml`.
        - Modify the `send_alert` function in `monitor.py` to use the chosen API to send alerts.

### Containerization (Optional - Docker)

1. **Build Docker Image:**

   - Navigate to the project directory containing `Dockerfile`.
   - Build the Docker image:

     ```bash
     docker build -t pipeline-monitor .
     ```

2. **Run with Docker Compose (Optional):**

   - If you have `docker-compose.yml`, you can run the monitor along with Prometheus and Grafana using:

     ```bash
     docker-compose up
     ```

   - Refer to the `docker-compose.yml` file for details on how Prometheus and Grafana are configured (if provided).

## Project Files

- `monitor.py`: The main Python script for the health monitor.
- `config.yaml`: Configuration file for thresholds and settings.
- `sample_jenkins.log`: Sample Jenkins log file for testing.
- `README.md`: This documentation file.
- `Dockerfile` (Optional): Dockerfile for containerization.
- `docker-compose.yml` (Optional): Docker Compose file for running with Prometheus and Grafana.
- `dashboard.json` (Optional): Sample Grafana dashboard configuration.

## Deliberate Inefficiencies (for Demonstration)

- **Simple Log Parsing:** The current log parsing in `parse_jenkins_log` is very basic and might not be robust enough for complex Jenkins log formats. In a real-world scenario, more sophisticated parsing techniques (e.g., using regular expressions or dedicated log parsing libraries) would be necessary.
- **Sequential Log Processing:** The monitor processes the log file sequentially in each interval. For very large log files, this could become inefficient.  Improvements could include:
    - Processing logs incrementally or using techniques to only parse new log entries.
    - Using asynchronous processing or multi-threading for log parsing.
- **Basic Alerting:** The alerting mechanism is currently limited to printing to the console. Real-world alerting systems would require integration with dedicated notification services like Slack, email, PagerDuty, etc., with proper error handling and retry mechanisms.

These inefficiencies are included to highlight areas for potential improvement and optimization in a production-ready monitoring solution. Addressing these could lead to significant performance gains, such as a hypothetical **40% reduction in debugging time** due to faster metric updates and more effective alerting.
