# Log File Analyzer for Intrusion Detection

A comprehensive Python-based tool for analyzing system log files to detect potential security threats and intrusion attempts. This project is designed to run in a Linux environment (tested on Kali Linux).

## Features

- Log file analysis for security threats
- Real-time or batch log analysis
- Visual representation of security events
- Incident report export (CSV format)
- Support for various log formats (Apache, auth)
- Customizable detection patterns

## Prerequisites

- Python 3.x
- Kali Linux (or any Linux distribution)
- Required Python packages:
  ```bash
  pip3 install matplotlib pandas
  ```

## Project Structure

```
.
├── src/
│   ├── main.py           # Project entry point for analysis and reporting
│   ├── parsers.py        # Log parsing utilities (Apache, auth logs)
│   ├── detectors.py      # Intrusion detection logic (SSH brute-force, HTTP flood, scanning)
│   ├── visualizers.py    # Data visualization tools
│   ├── reporter.py       # Incident and preview export
│   └── blacklist.py      # (Optional) IP blacklist checking utilities
├── data/                 # Place your input log files and custom blacklist .txt files here
├── reports/              # Output folder for generated incident reports and visualization graphs
├── _docs/                # Documentation
└── README.md
```

- **data/**: Place your raw log files (for example, access.log, auth.log) here before analysis.
  You can also put any text-based blacklist files for IP reputation checking in this folder.
  Example contents:

  - access.log — Apache web server access log
  - auth.log — Linux system authentication log
  - blacklist_ips.txt — List of known malicious IP addresses

- **reports/**: This directory will be created automatically if it doesn't exist. After running the analyzer, reports like `incidents.csv` and visualization images (e.g., `top_ips.png`, `requests_time.png`) will appear here.  
  Example contents:

  - incidents.csv — Detected suspicious events and intrusion attempts
  - top_ips.png — Bar graph of the most active IP addresses
  - requests_time.png — Line chart of requests over time
  - log_preview.csv — Sample of parsed log entries for review

- Both folders are excluded from version control by default (using `.gitignore`) and will be created as needed.

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/CodeWithAK28/Log-File-Analyzer-for-Intrusion-Detection---Cyber-Security-Project.git
   cd Log-File-Analyzer-for-Intrusion-Detection---Cyber-Security-Project
   ```

2. Set up Python environment as needed.

## Usage

### 1. Run the Analyzer

To analyze log files and generate incident reports and graphs:

```bash
python3 src/main.py
```

- Incidents are exported to `reports/incidents.csv`
- Preview of parsed logs to `reports/log_preview.csv`
- Top IPs graph: `reports/top_ips.png`
- Request time graph: `reports/requests_time.png`

Place your log files in the `data/` directory.

### 2. Custom Utility Scripts

- **Log Parsing**: `src/parsers.py` contains direct parsing functions for Apache/auth logs (for integration or standalone use).
- **Detection & Visualization**: Use individual scripts (`detectors.py`, `visualizers.py`) for custom workflows.
- **Blacklist Checking**: `src/blacklist.py` provides helpers to check IPs against local blacklists in `data/`.

### 3. Customization

- Tune detection thresholds in `detectors.py`
- Adjust chart appearance in `visualizers.py`
- Modify or add new parsers for different log formats in `parsers.py`
- Place blacklists/allow lists as `.txt` files in `data/` and use `blacklist.py` functions.

## Security Patterns Detected

- Failed password/SSH brute force attempts
- HTTP flood attacks
- Web scanning/probing of multiple paths
- (Extendable: detection logic in `detectors.py`)

## Best Practices

1. Regular Updates:

   ```bash
   git pull origin main
   ```

2. Log Rotation:
   Ensure your system has proper log rotation configured to manage log file sizes.

3. Incident/Database Maintenance:
   Regularly backup your `reports/` directory:
   ```bash
   cp reports/incidents.csv reports/incidents.backup.csv
   ```

## Troubleshooting

1. Permission Issues:

   ```bash
   sudo chmod 644 data/*.log
   ```

2. Python Package Issues:
   ```bash
   pip3 install --upgrade matplotlib pandas
   ```

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a new Pull Request

## License

This project is licensed under the MIT License – see the LICENSE file for details.

## Acknowledgments

- Based on common Linux log analysis patterns
- Inspired by real-world intrusion detection systems
- Developed for educational purposes

---

### Expected Result

After running the analyzer:

- Suspicious IPs and detected attacks (e.g., HTTP flood, SSH brute-force) are exported to `reports/incidents.csv`
- Visualization graphs are saved in the `reports/` folder:
  - `top_ips.png` → Most active IP addresses
  - `requests_time.png` → Request activity over time

✅ **Final Outcome**

The analyzer successfully detects and reports intrusion patterns, providing a quick and automated way to analyze log data and identify potential threats.
