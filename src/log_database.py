#!/usr/bin/env python3

import sqlite3
import argparse
from datetime import datetime


class LogDatabase:
    def __init__(self, db_name='log_events.db'):
        self.db_name = db_name
        self.init_database()

    def init_database(self):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        # Create tables for storing log events
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS security_events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME,
                event_type TEXT,
                source_ip TEXT,
                description TEXT,
                severity INTEGER
            )
        ''')

        conn.commit()
        conn.close()

    def store_event(self, event_type, source_ip, description, severity=1):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        timestamp = datetime.now()
        cursor.execute('''
            INSERT INTO security_events 
            (timestamp, event_type, source_ip, description, severity)
            VALUES (?, ?, ?, ?, ?)
        ''', (timestamp, event_type, source_ip, description, severity))

        conn.commit()
        conn.close()

    def query_events(self, event_type=None, start_time=None, end_time=None):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        query = "SELECT * FROM security_events WHERE 1=1"
        params = []

        if event_type:
            query += " AND event_type = ?"
            params.append(event_type)

        if start_time:
            query += " AND timestamp >= ?"
            params.append(start_time)

        if end_time:
            query += " AND timestamp <= ?"
            params.append(end_time)

        cursor.execute(query, params)
        results = cursor.fetchall()
        conn.close()

        return results


def main():
    parser = argparse.ArgumentParser(
        description='Store and query log events in SQLite database')
    parser.add_argument('--action', choices=['store', 'query'], required=True,
                        help='Action to perform: store new event or query existing events')
    args = parser.parse_args()

    db = LogDatabase()

    if args.action == 'store':
        # Example of storing an event
        db.store_event(
            event_type='failed_login',
            source_ip='192.168.1.100',
            description='Multiple failed login attempts',
            severity=2
        )
    else:
        # Example of querying events
        events = db.query_events(event_type='failed_login')
        for event in events:
            print(event)


if __name__ == "__main__":
    main()
