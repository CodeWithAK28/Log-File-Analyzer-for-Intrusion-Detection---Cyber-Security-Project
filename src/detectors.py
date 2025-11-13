# src/detectors.py
import pandas as pd
from datetime import timedelta


def detect_ssh_bruteforce(df, time_window_minutes=10, attempt_threshold=20):
    df = df[df['service'] == 'ssh'].dropna(subset=['ip'])
    df = df.sort_values('timestamp')

    alerts = []
    grouped = df.groupby('ip')

    for ip, group in grouped:
        times = group['timestamp'].sort_values().reset_index(drop=True)

        for j in range(len(times)):
            while times[j] - times[0] > timedelta(minutes=time_window_minutes):
                times = times.drop(0).reset_index(drop=True)

            window_size = j - 0 + 1
            if window_size >= attempt_threshold:
                alerts.append({
                    'ip': ip,
                    'type': 'ssh_bruteforce',
                    'count': int(window_size),
                    'start': times[0],
                    'end': times[j]
                })
                break

    return pd.DataFrame(alerts)


def detect_http_flood(df, per_min_threshold=200):
    # Filter only Apache service entries
    df = df[df.get('service') == 'apache'].copy()

    if df.empty:
        print("[+] No Apache logs found for HTTP flood detection.")
        return pd.DataFrame([])

    # Ensure timestamp is datetime
    if not pd.api.types.is_datetime64_any_dtype(df['timestamp']):
        print("[+] Converting timestamp to datetime for HTTP flood detection ...")
        df['timestamp'] = pd.to_datetime(
            df['timestamp'], errors='coerce', utc=True)

    # Drop rows with invalid timestamps
    df = df.dropna(subset=['timestamp'])
    if df.empty:
        print("[!] All timestamps invalid in HTTP flood detection.")
        return pd.DataFrame([])

    # Floor timestamps to nearest minute
    df['minute'] = df['timestamp'].dt.floor('T')

    # Count requests per IP per minute
    agg = df.groupby(['ip', 'minute']).size().reset_index(name='reqs')

    # Identify suspicious IPs
    suspicious = agg[agg['reqs'] >= per_min_threshold].copy()

    if suspicious.empty:
        print("[+] No HTTP flood detected.")
        return pd.DataFrame([])

    suspicious['type'] = 'http_flood'
    print(f"[!!] Detected possible HTTP flood from {len(suspicious)} IP(s).")

    return suspicious


def detect_scanning(df, unique_path_threshold=100, time_window_minutes=10):
    df = df[df['service'] == 'apache'].sort_values('timestamp')

    alerts = []
    grouped = df.groupby('ip')

    for ip, group in grouped:
        cutoff = group['timestamp'].max(
        ) - pd.Timedelta(minutes=time_window_minutes)
        recent = group[group['timestamp'] >= cutoff]

        unique_paths = recent['path'].nunique()

        if unique_paths >= unique_path_threshold:
            alerts.append({
                'ip': ip,
                'type': 'scanning',
                'unique_paths': int(unique_paths),
                'window_start': recent['timestamp'].min(),
                'window_end': recent['timestamp'].max()
            })

    return pd.DataFrame(alerts)
