from pathlib import Path
import pandas as pd

# Paths
ROOT = Path(__file__).resolve().parents[1]
INPUT_FILE = ROOT / "data" / "channels.xlsx"
OUTPUT_FILE = ROOT / "output" / "playlist.m3u"

# Read Excel
df = pd.read_excel(INPUT_FILE)

# Make sure output folder exists
OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

lines = ["#EXTM3U"]

for _, row in df.iterrows():

    name = str(row.get("Channel Name", "")).strip()
    group = str(row.get("Group", "")).strip()
    url = str(row.get("Stream URL", "")).strip()
    status = str(row.get("Status", "")).strip().lower()

    # skip empty or inactive rows
    if not name or not url:
        continue
    if status and status != "active":
        continue

    extinf = f'#EXTINF:-1 group-title="{group}",{name}'
    lines.append(extinf)
    lines.append(url)

# Write file
OUTPUT_FILE.write_text("\n".join(lines), encoding="utf-8")

print("Playlist created successfully at:", OUTPUT_FILE)
