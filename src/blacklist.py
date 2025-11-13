# src/blacklist.py
from pathlib import Path


def load_blocklist(path):
    return set(line.strip() for line in Path(path).read_text().splitlines() if line.strip() and not line.startswith('#'))


def check_local_blacklists(ip, lists_dir='data'):
    result = {}
    d = Path(lists_dir)
    if not d.exists():
        return result
    for fname in d.glob("*.txt"):
        name = fname.stem
        try:
            ips = load_blocklist(fname)
            result[name] = ip in ips
        except Exception:
            result[name] = False
    return result
