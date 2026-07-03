from pathlib import Path
import pandas as pd

# ==========================================================
# Paths
# ==========================================================

ROOT = Path(__file__).resolve().parents[1]

INPUT_FILE = ROOT / "data" / "channels.xlsx"
OUTPUT_FILE = ROOT / "output" / "playlist.m3u"

# Put your XMLTV EPG URL here
EPG_URL = "https://your-epg-url.xml"

# ==========================================================
# Read Excel
# ==========================================================

df = pd.read_excel(INPUT_FILE).fillna("")

# Remove leading/trailing spaces from column names
df.columns = df.columns.str.strip()

# ==========================================================
# Keep only active channels
# ==========================================================

if "Status" in df.columns:
    df = df[df["Status"].astype(str).str.lower().str.strip() == "active"]

# ==========================================================
# Remove empty rows
# ==========================================================

df = df[
    (df["Channel Name"].astype(str).str.strip() != "") &
    (df["Stream URL"].astype(str).str.strip() != "")
]

# ==========================================================
# Remove duplicate URLs
# ==========================================================

df = df.drop_duplicates(subset=["Stream URL"])

# Uncomment the next line if you also want duplicate
# channel names removed.

# df = df.drop_duplicates(subset=["Channel Name"])

# ==========================================================
# Sort
# ==========================================================

if "Group" in df.columns:
    df = df.sort_values(
        by=["Group", "Channel Name"],
        na_position="last"
    )
else:
    df = df.sort_values(by=["Channel Name"])

# ==========================================================
# Create output folder
# ==========================================================

OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

lines = [
    f'#EXTM3U x-tvg-url="{EPG_URL}"'
]

# ==========================================================
# Build playlist
# ==========================================================

for _, row in df.iterrows():

    name = str(row.get("Channel Name", "")).strip()
    url = str(row.get("Stream URL", "")).strip()

    attrs = []

    epg = str(row.get("EPG ID", "")).strip()
    if epg:
        attrs.append(f'tvg-id="{epg}"')

    logo = str(row.get("Logo", "")).strip()
    if logo:
        attrs.append(f'tvg-logo="{logo}"')

    group = str(row.get("Group", "")).strip()
    if group:
        attrs.append(f'group-title="{group}"')

    country = str(row.get("Country", "")).strip()
    if country:
        attrs.append(f'tvg-country="{country}"')

    language = str(row.get("Language", "")).strip()
    if language:
        attrs.append(f'tvg-language="{language}"')

    resolution = str(row.get("Resolution", "")).strip()
    if resolution:
        attrs.append(f'tvg-resolution="{resolution}"')

    extinf = "#EXTINF:-1"

    if attrs:
        extinf += " " + " ".join(attrs)

    extinf += f",{name}"

    lines.append(extinf)
    lines.append(url)

# ==========================================================
# Save
# ==========================================================

OUTPUT_FILE.write_text(
    "\n".join(lines),
    encoding="utf-8"
)

# ==========================================================
# Statistics
# ==========================================================

print("=" * 50)
print("Playlist created successfully!")
print(f"Channels : {len(df)}")
print(f"Saved to : {OUTPUT_FILE}")
print("=" * 50)
