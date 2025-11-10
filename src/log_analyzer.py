#!/usr/bin/env python3

import sys
import re
import argparse
from datetime import datetime


class LogAnalyzer:
    def __init__(self):
        self.suspicious_patterns = [
            r'Failed password',
            r'Invalid user',
            r'Authentication failure',
            r'Connection closed by authenticating user',
            r'Bad protocol version identification',
            r'Did not receive identification string',
            r'error: maximum authentication attempts exceeded'
        ]

    def analyze_log(self, log_file):
        try:
            with open(log_file, 'r') as f:
                for line in f:
                    self.check_line(line.strip())
        except FileNotFoundError:
            print(f"Error: File {log_file} not found")
            sys.exit(1)

    def check_line(self, line):
        for pattern in self.suspicious_patterns:
            if re.search(pattern, line):
                print(f"[ALERT] Suspicious activity detected: {line}")


def main():
    parser = argparse.ArgumentParser(
        description='Analyze log files for potential security threats')
    parser.add_argument('log_file', help='Path to the log file to analyze')
    args = parser.parse_args()

    analyzer = LogAnalyzer()
    analyzer.analyze_log(args.log_file)


if __name__ == "__main__":
    main()
