from pathlib import Path
import pandas as pd

# ==========================
# Paths
# ==========================
ROOT = Path(__file__).resolve().parents[1]

INPUT_FILE = ROOT / "data" / "channels.xlsx"
OUTPUT_FILE = ROOT / "output" / "playlist.m3u"

# ==========================
# Read Excel
# ==========================
df = pd.read_excel(INPUT_FILE).fillna("")

# Create output folder
OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

lines = ["#EXTM3U"]

for _, row in df.iterrows():

    name = str(row.get("Channel Name", "")).strip()
    url = str(row.get("Stream URL", "")).strip()

    if not name or not url:
        continue

    status = str(row.get("Status", "active")).strip().lower()
    if status != "active":
        continue

    group = str(row.get("Group", "")).strip()
    logo = str(row.get("Logo", "")).strip()
    epg = str(row.get("EPG ID", "")).strip()
    country = str(row.get("Country", "")).strip()
    language = str(row.get("Language", "")).strip()
    resolution = str(row.get("Resolution", "")).strip()

    attrs = []

    if epg:
        attrs.append(f'tvg-id="{epg}"')

    if logo:
        attrs.append(f'tvg-logo="{logo}"')

    if group:
        attrs.append(f'group-title="{group}"')

    if country:
        attrs.append(f'tvg-country="{country}"')

    if language:
        attrs.append(f'tvg-language="{language}"')

    if resolution:
        attrs.append(f'tvg-resolution="{resolution}"')

    extinf = f'#EXTINF:-1 {" ".join(attrs)},{name}'

    lines.append(extinf)
    lines.append(url)

OUTPUT_FILE.write_text("\n".join(lines), encoding="utf-8")

print("Playlist created successfully!")
print("Saved to:", OUTPUT_FILE)
