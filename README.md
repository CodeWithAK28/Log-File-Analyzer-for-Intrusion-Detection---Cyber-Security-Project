# Log File Analyzer for Intrusion Detection

A comprehensive Python-based tool for analyzing system log files to detect potential security threats and intrusion attempts. This project is designed to run in a Linux environment (tested on Kali Linux) and provides various tools for log analysis, visualization, and real-time monitoring.

## Features

- Log file analysis for security threats
- Real-time log monitoring with alerts
- Visual representation of security events
- Database storage for log events
- Support for various log formats
- Customizable detection patterns

## Prerequisites

- Python 3.x
- Kali Linux (or any Linux distribution)
- Required Python packages:
  ```bash
  pip3 install matplotlib
  pip3 install sqlite3
  ```

## Project Structure

```
.
├── src/
│   ├── log_analyzer.py    # Core log analysis functionality
│   ├── log_visualizer.py  # Data visualization tools
│   ├── log_monitor.py     # Real-time log monitoring
│   └── log_database.py    # Database operations for log events
├── _docs/                 # Documentation
└── README.md
```

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/CodeWithAK28/Log-File-Analyzer-for-Intrusion-Detection---Cyber-Security-Project.git
   cd Log-File-Analyzer-for-Intrusion-Detection---Cyber-Security-Project
   ```

2. Make the Python scripts executable:
   ```bash
   chmod +x src/*.py
   ```

## Usage

### 1. Log Analysis

Analyze a log file for potential security threats:

```bash
python3 src/log_analyzer.py /var/log/auth.log
```

### 2. Visualization

Generate visual representations of log data:

```bash
python3 src/log_visualizer.py
```

This will create:

- IP frequency chart (ip_frequency.png)
- Event distribution pie chart (event_distribution.png)

### 3. Real-time Monitoring

Monitor log files in real-time for security events:

```bash
python3 src/log_monitor.py /var/log/auth.log
```

### 4. Database Operations

Store and query log events:

```bash
# Store events
python3 src/log_database.py --action store

# Query events
python3 src/log_database.py --action query
```

## Configuration

- Modify suspicious patterns in `log_analyzer.py`
- Adjust alert thresholds in `log_monitor.py`
- Customize visualization settings in `log_visualizer.py`
- Configure database settings in `log_database.py`

## Security Patterns Detected

- Failed password attempts
- Invalid user login attempts
- Authentication failures
- Suspicious IP addresses
- Brute force attempts
- Connection anomalies

## Best Practices

1. Regular Updates:

   ```bash
   git pull origin main
   ```

2. Log Rotation:
   Ensure your system has proper log rotation configured to manage log file sizes.

3. Database Maintenance:
   Regularly backup the SQLite database:
   ```bash
   cp log_events.db log_events.backup.db
   ```

## Troubleshooting

1. Permission Issues:

   ```bash
   sudo chmod 644 /var/log/auth.log
   ```

2. Python Package Issues:
   ```bash
   pip3 install --upgrade matplotlib sqlite3
   ```

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a new Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Based on common Linux log analysis patterns
- Inspired by real-world intrusion detection systems
- Developed for educational purposes

## Contact

- GitHub: [@CodeWithAK28](https://github.com/CodeWithAK28)

Goal

To identify intrusion patterns from raw log files, visualize access trends, and generate a clear incident report for cybersecurity analysis and response.

Overview of Tools & Libraries Used

Python 3.10+ — core programming language

pandas — data handling and analysis

matplotlib — data visualization

regex (re) — log pattern extraction

python-dateutil — timestamp parsing

requests (optional) — for checking IP reputation or blacklist info

Expected Result

After running the analyzer:

Suspicious IPs and detected attacks (e.g., HTTP flood, SSH brute-force) are exported to reports/incidents.csv

Visualization graphs are saved in the reports/ folder, showing:

top_ips.png → Most active IP addresses

requests_time.png → Request activity over time

✅ Final Outcome

The analyzer successfully detects and reports intrusion patterns, providing a quick and automated way to analyze log data and identify potential threats.
