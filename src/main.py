# main.py
from pathlib import Path
import pandas as pd
from parsers import parse_apache_log, parse_auth_log
from detectors import detect_ssh_bruteforce, detect_http_flood, detect_scanning
from reporter import export_incidents, save_dataframe_preview
from visualizers import plot_top_ips, plot_requests_over_time

DATA_DIR = Path("data")   # ← change to "logs" if you put logs there
REPORT_DIR = Path("reports")


def ensure_timestamp(df):
    if df is None or df.empty:
        return df
    if 'timestamp' in df.columns:
        print(f"[!] Converting timestamp for {len(df)} rows")
        df['timestamp'] = pd.to_datetime(
            df['timestamp'], errors="coerce", utc=True)
        if df['timestamp'].isna().all():
            print(
                "[!] Warning: All timestamps failed to convert – check your parser output.")
            print(df.head())
    else:
        print("[!] No 'timestamp' column found.")
    return df


def main():
    REPORT_DIR.mkdir(exist_ok=True)
    DATA_DIR.mkdir(exist_ok=True)

    # ── Parse logs (pass file paths to parsers) ──
    apache_df = parse_apache_log(
        DATA_DIR / "access.log") if (DATA_DIR / "access.log").exists() else pd.DataFrame([])

    ssh_df = parse_auth_log(
        DATA_DIR / "auth.log") if (DATA_DIR / "auth.log").exists() else pd.DataFrame([])

    # add service column so detectors can filter
    if not apache_df.empty:
        apache_df['service'] = "apache"
    if not ssh_df.empty:
        ssh_df['service'] = "ssh"

    # normalize timestamps into datetimes (so .dt works)
    apache_df = ensure_timestamp(apache_df)
    ssh_df = ensure_timestamp(ssh_df)

    # combined df
    combined = pd.concat([apache_df, ssh_df], ignore_index=True, sort=False)

    if combined.empty:
        print("[!] No log data found in data/access.log or data/auth.log")
        return

    # ── Run detectors ──
    print("[+] Running detectors ...")
    bruteforce = detect_ssh_bruteforce(combined)
    flood = detect_http_flood(combined)
    scan = detect_scanning(combined)

    # ── Export incidents ──
    parts = [d for d in (bruteforce, flood, scan)
             if (d is not None and not d.empty)]
    incidents = pd.concat(parts, ignore_index=True,
                          sort=False) if parts else pd.DataFrame([])

    if not incidents.empty:
        export_incidents(incidents, REPORT_DIR / "incidents.csv")
    else:
        print("[+] No suspicious incidents detected.")

    # ── Save preview + plots ──
    save_dataframe_preview(combined, REPORT_DIR / "log_preview.csv")
    plot_top_ips(combined, out_path=str(REPORT_DIR / "top_ips.png"))
    plot_requests_over_time(combined, out_path=str(
        REPORT_DIR / "requests_time.png"))

    print("[✓] Done. Check the 'reports/' folder.")


if __name__ == "__main__":
    main()
