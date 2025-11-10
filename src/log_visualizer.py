#!/usr/bin/env python3

import re
from collections import Counter
import matplotlib.pyplot as plt
from datetime import datetime


class LogVisualizer:
    def __init__(self):
        self.ip_pattern = r'\b(?:\d{1,3}\.){3}\d{1,3}\b'
        self.timestamp_pattern = r'\b\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\b'

    def analyze_log(self, log_file):
        ip_addresses = []
        timestamps = []
        events = []

        with open(log_file, 'r') as f:
            for line in f:
                # Extract IP addresses
                ips = re.findall(self.ip_pattern, line)
                ip_addresses.extend(ips)

                # Extract timestamps
                timestamp = re.search(self.timestamp_pattern, line)
                if timestamp:
                    timestamps.append(datetime.strptime(
                        timestamp.group(), '%Y-%m-%d %H:%M:%S'))

                # Extract event types
                if 'Failed password' in line:
                    events.append('Failed Login')
                elif 'Invalid user' in line:
                    events.append('Invalid User')
                elif 'Authentication failure' in line:
                    events.append('Auth Failure')

        return ip_addresses, timestamps, events

    def create_visualizations(self, ip_addresses, timestamps, events):
        # IP address frequency
        ip_freq = Counter(ip_addresses)
        plt.figure(figsize=(12, 6))
        plt.bar(ip_freq.keys(), ip_freq.values())
        plt.xticks(rotation=45)
        plt.title('Frequency of IP Addresses')
        plt.tight_layout()
        plt.savefig('ip_frequency.png')

        # Event type distribution
        event_freq = Counter(events)
        plt.figure(figsize=(8, 8))
        plt.pie(event_freq.values(), labels=event_freq.keys(), autopct='%1.1f%%')
        plt.title('Distribution of Event Types')
        plt.savefig('event_distribution.png')


def main():
    visualizer = LogVisualizer()
    ip_addresses, timestamps, events = visualizer.analyze_log('auth.log')
    visualizer.create_visualizations(ip_addresses, timestamps, events)


if __name__ == "__main__":
    main()
