from pathlib import Path
import pandas as pd

# Project folders
ROOT = Path(__file__).resolve().parents[1]
EXCEL_FILE = ROOT / "data" / "channels.xlsx"
OUTPUT_FILE = ROOT / "output" / "playlist.m3u"

# Read Excel
df = pd.read_excel(EXCEL_FILE)

# Create output folder if needed
OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    f.write("#EXTM3U\n")

    for _, row in df.iterrows():

        # Skip inactive channels
        status = str(row.get("Status", "")).strip().lower()
        if status != "active":
            continue

        name = str(row.get("Channel Name", "")).strip()
        group = str(row.get("Group", "")).strip()
        logo = str(row.get("Logo", "")).strip()
        epg = str(row.get("EPG ID", "")).strip()
        url = str(row.get("Stream URL", "")).strip()

        if not name or not url:
            continue

        extinf = '#EXTINF:-1'

        if epg and epg != "nan":
            extinf += f' tvg-id="{epg}"'

        if logo and logo != "nan":
            extinf += f' tvg-logo="{logo}"'

        if group and group != "nan":
            extinf += f' group-title="{group}"'

        extinf += f',{name}'

        f.write(extinf + "\n")
        f.write(url + "\n")

print("Playlist created successfully!")
