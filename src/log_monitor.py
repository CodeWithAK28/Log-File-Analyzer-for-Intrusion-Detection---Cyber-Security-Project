#!/usr/bin/env python3

import os
import argparse
import subprocess
from datetime import datetime


class LogMonitor:
    def __init__(self, log_file):
        self.log_file = log_file
        self.last_position = 0
        self.alert_thresholds = {
            'failed_login': 5,  # Alert after 5 failed login attempts
            'invalid_user': 3,  # Alert after 3 invalid user attempts
            'auth_failure': 3   # Alert after 3 authentication failures
        }

    def monitor(self):
        try:
            while True:
                with open(self.log_file, 'r') as f:
                    f.seek(self.last_position)
                    new_lines = f.readlines()
                    self.last_position = f.tell()

                    if new_lines:
                        self.analyze_new_lines(new_lines)

        except KeyboardInterrupt:
            print("\nMonitoring stopped by user")

    def analyze_new_lines(self, lines):
        failed_logins = 0
        invalid_users = 0
        auth_failures = 0

        for line in lines:
            if 'Failed password' in line:
                failed_logins += 1
            elif 'Invalid user' in line:
                invalid_users += 1
            elif 'Authentication failure' in line:
                auth_failures += 1

        # Check thresholds and send alerts
        if failed_logins >= self.alert_thresholds['failed_login']:
            self.send_alert(
                f"High number of failed login attempts: {failed_logins}")

        if invalid_users >= self.alert_thresholds['invalid_user']:
            self.send_alert(
                f"Multiple invalid user attempts detected: {invalid_users}")

        if auth_failures >= self.alert_thresholds['auth_failure']:
            self.send_alert(
                f"Multiple authentication failures detected: {auth_failures}")

    def send_alert(self, message):
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        alert = f"[{timestamp}] ALERT: {message}"
        print(alert)
        # In a real implementation, you might want to:
        # - Send email notifications
        # - Write to a separate alert log
        # - Trigger system notifications
        # - Take automated response actions


def main():
    parser = argparse.ArgumentParser(
        description='Monitor log files for security events in real-time')
    parser.add_argument('log_file', help='Path to the log file to monitor')
    args = parser.parse_args()

    monitor = LogMonitor(args.log_file)
    monitor.monitor()


if __name__ == "__main__":
    main()
