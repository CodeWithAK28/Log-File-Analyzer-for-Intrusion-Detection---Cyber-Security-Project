# src/visualizer.py
import matplotlib.pyplot as plt
from pathlib import Path


def plot_top_ips(df, top_n=10, out_path="reports/top_ips.png"):
    counts = df.groupby('ip').size().sort_values(ascending=False).head(top_n)

    ax = counts.plot.bar()
    ax.set_title("Top IPs by events")
    ax.set_xlabel("IP")
    ax.set_ylabel("Event count")

    Path(out_path).parent.mkdir(parents=True, exist_ok=True)
    plt.tight_layout()
    plt.savefig(out_path)
    plt.close()


def plot_requests_over_time(df, ip=None, freq='1T', out_path="reports/requests_time.png"):
    if ip:
        df = df[df['ip'] == ip]

    ts = df.set_index('timestamp').resample(freq).size()

    ax = ts.plot()
    ax.set_title(f"Requests over time {'for ' + ip if ip else ''}")
    ax.set_xlabel("Time")
    ax.set_ylabel("Requests")

    Path(out_path).parent.mkdir(parents=True, exist_ok=True)
    plt.tight_layout()
    plt.savefig(out_path)
    plt.close()
