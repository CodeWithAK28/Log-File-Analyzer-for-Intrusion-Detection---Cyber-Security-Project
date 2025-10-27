 Log File Analyzer for Intrusion Detection
 Objective

To develop a Python-based tool that automatically analyzes system and web server logs (Apache & SSH) to detect suspicious or malicious activities such as brute-force attacks, HTTP floods, and scanning behavior.

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
