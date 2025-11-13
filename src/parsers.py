import re
import pandas as pd
from pathlib import Path


def parse_apache_log(file_path):
    """
    Parses Apache access logs into a DataFrame.

    Expected log format example:
    127.0.0.1 - - [01/Oct/2023:13:55:36 +0530] "GET /index.html HTTP/1.1" 200 1024
    """

    # Regex pattern for Apache logs
    pattern = (
        r'(\S+)\s+'
        r'\S+\s+\S+\s+'
        r'\[([^]]+)\]\s+'
        r'"(\S+)\s+(\S+)\s+(\S+)"\s+'
        r'(\d+)\s+(\d+)'
    )

    log_path = Path(file_path)
    if not log_path.exists():
        print(f"[-] File not found: {file_path}")
        return pd.DataFrame()

    with open(log_path, encoding='utf-8', errors='ignore') as f:
        matches = re.findall(pattern, f.read())

    if not matches:
        print("[-] No Apache log entries found.")
        return pd.DataFrame()

    # Create DataFrame
    df = pd.DataFrame(
        matches,
        columns=['ip', 'timestamp', 'method',
                 'path', 'protocol', 'status', 'size']
    )

    print(f"[+] Converting timestamp for {len(df)} rows")
    df['timestamp'] = pd.to_datetime(
        df['timestamp'],
        format='%d/%b/%Y:%H:%M:%S %z',
        errors='coerce'
    )

    if df['timestamp'].isna().all():
        print(
            "[!] Warning: All timestamps failed to convert — check your parser output.")

    # Convert numbers
    df['status'] = pd.to_numeric(df['status'], errors='coerce')
    df['size'] = pd.to_numeric(df['size'], errors='coerce')

    # Label this log source
    df['service'] = 'apache'
    return df


def parse_auth_log(file_path):
    """
    Parses authentication logs for failed login attempts.

    Example:
    Oct 10 10:00:00 server sshd[1234]: Failed password for root from 192.168.1.5 port 22 ssh2
    """

    pattern = (
        r'([A-Za-z]{3}\s+\d{1,2}\s+\d\d:\d\d:\d\d)\s+\S+\s+sshd\[\d+\]:\s+'
        r'Failed password for (\S+)\s+from\s+(\d+\.\d+\.\d+\.\d+)'
    )

    log_path = Path(file_path)
    if not log_path.exists():
        print(f"[-] File not found: {file_path}")
        return pd.DataFrame()

    with open(log_path, encoding='utf-8', errors='ignore') as f:
        matches = re.findall(pattern, f.read())

    if not matches:
        print("[-] No authentication log entries found.")
        return pd.DataFrame()

    df = pd.DataFrame(matches, columns=['timestamp', 'user', 'ip'])

    print(f"[+] Converting timestamp for {len(df)} rows")
    df['timestamp'] = pd.to_datetime(
        df['timestamp'],
        format='%b %d %H:%M:%S',
        errors='coerce'
    )

    if df['timestamp'].isna().all():
        print(
            "[!] Warning: All timestamps failed to convert — check your parser output.")

    df['service'] = 'auth'
    return df


def load_combined_logs(data_dir):
    """
    Loads Apache and Auth logs (if available) into one combined DataFrame.
    """

    data_dir = Path(data_dir)
    apache_path = data_dir / 'access.log'
    auth_path = data_dir / 'auth.log'

    apache_df = parse_apache_log(
        apache_path) if apache_path.exists() else pd.DataFrame()
    auth_df = parse_auth_log(
        auth_path) if auth_path.exists() else pd.DataFrame()

    if not apache_df.empty and not auth_df.empty:
        combined = pd.concat([apache_df, auth_df], ignore_index=True)
    elif not apache_df.empty:
        combined = apache_df
    elif not auth_df.empty:
        combined = auth_df
    else:
        combined = pd.DataFrame()

    return combined
