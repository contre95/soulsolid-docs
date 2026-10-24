#!/usr/bin/env python3
"""Generate a small, fictional, fully tagged music library for the static demo.

Every track is synthesized with ffmpeg (no copyrighted audio), gets a generated
cover, and carries enough tags (genre, year, ISRC, BPM, lyrics...) to make the
library, metrics and analyze pages look like a real collection. A few
imperfections are added on purpose so the analyze/merge pages have something
to show: genre spelling variants and missing tags.

Usage: gen_library.py <output_dir> [--dupes <dir>]
  <output_dir>  tracks to import into the library
  --dupes       retagged copies of a few tracks, imported afterwards so they
                land in the import queue as duplicates
"""

import argparse
import hashlib
import os
import shutil
import subprocess
import sys
import tempfile

CATALOG = [
    {
        "artist": "Velvet Static", "album": "Neon Tides", "year": 2019, "genre": "Synthwave",
        "label": "Lunar Grid Records", "type": "album", "format": "flac", "colors": ("0x1b1464", "0xff2a6d"),
        "tracks": ["Midnight Arcade", "Chrome Horizon", "Neon Tides", "Pulse Runner", "Afterglow Drive", "Static Hearts"],
    },
    {
        "artist": "Velvet Static", "album": "Signal Lost", "year": 2022, "genre": "Synthwave",
        "label": "Lunar Grid Records", "type": "ep", "format": "mp3", "colors": ("0x05d9e8", "0x01012b"),
        "tracks": ["Signal Lost", "Dead Air", "Carrier Wave", "Off the Grid"],
    },
    {
        "artist": "The Paper Lanterns", "album": "Harbor Lights", "year": 2015, "genre": "Indie Folk",
        "label": "Driftwood", "type": "album", "format": "flac", "colors": ("0xf4a259", "0x5b8e7d"),
        "tracks": ["Harbor Lights", "Saltwater Letters", "The Long Way Home", "Lantern Song", "Gulls", "Low Tide", "Northern Shore"],
    },
    {
        "artist": "Mara Quell", "album": "Concrete Bloom", "year": 2021, "genre": "Hip-Hop",
        "label": "Blockparty Sound", "type": "album", "format": "mp3", "colors": ("0x2b2d42", "0xef233c"),
        "tracks": ["Concrete Bloom", "Corner Store Prophet", "Rooftop", "Late Train", "Bloom (Reprise)"],
    },
    {
        "artist": "Mara Quell", "album": "Blue Hour", "year": 2023, "genre": "Hip Hop",  # spelling variant on purpose
        "label": "Blockparty Sound", "type": "single", "format": "mp3", "colors": ("0x003049", "0x669bbc"),
        "tracks": ["Blue Hour"],
    },
    {
        "artist": "Orchid Engine", "album": "Low Orbit", "year": 2018, "genre": "Ambient",
        "label": "Stillpoint", "type": "album", "format": "flac", "colors": ("0x10002b", "0x9d4edd"),
        "tracks": ["Ascent", "Low Orbit", "Weightless", "Solar Wind", "Reentry"],
    },
    {
        "artist": "Ruben Okafor Trio", "album": "Night at the Lantern Club", "year": 2009, "genre": "Jazz",
        "label": "Smoke Ring", "type": "album", "format": "flac", "colors": ("0x432818", "0xbb9457"),
        "tracks": ["Opening Set", "Blue in Brass", "Rainy Tuesday", "Walking Bass Waltz", "Last Call"],
    },
    {
        "artist": "Glass Harbor", "album": "Fault Lines", "year": 2012, "genre": "Post-Rock",
        "label": "Tectonic", "type": "album", "format": "mp3", "colors": ("0x343a40", "0xadb5bd"),
        "tracks": ["Fault Lines", "Aftershock", "The Quiet Between", "Epicenter"],
    },
    {
        "artist": "Sunny Delacroix", "album": "Polaroid Summer", "year": 2024, "genre": "Pop",
        "label": "Candyfloss", "type": "album", "format": "mp3", "colors": ("0xffb703", "0xfb8500"),
        "tracks": ["Polaroid Summer", "Cherry Soda", "Bike Ride", "Sunburn", "Golden Hour"],
    },
    {
        "artist": "Various Artists", "album": "Lunar Grid Sampler Vol. 1", "year": 2020, "genre": "Electronic",
        "label": "Lunar Grid Records", "type": "compilation", "format": "mp3", "colors": ("0x000000", "0x39ff14"),
        "tracks": ["Grid Lock (Velvet Static)", "Satellite (Orchid Engine)", "Night Bus (Kite Collective)"],
    },
]

# Tracks without some tags, so the metadata analysis has gaps to report.
MISSING_GENRE = {("Glass Harbor", "Epicenter"), ("Sunny Delacroix", "Golden Hour")}
MISSING_YEAR = {("Glass Harbor", "Aftershock")}
NO_LYRICS_GENRES = {"Ambient", "Jazz", "Post-Rock"}

LYRICS = """I keep the window open for the {word} to come in
Counting all the colors that the night has never been
{title}, {title}
Hold the light a little longer than you should
{title}, {title}
I'd stay here forever if I could"""

NOTES = [220.0, 246.94, 261.63, 293.66, 329.63, 349.23, 392.0, 440.0]


def seed(*parts):
    return int(hashlib.sha1("|".join(map(str, parts)).encode()).hexdigest()[:8], 16)


def audio_expr(s, duration):
    """A short, unique, not-unpleasant synthesized loop for each track."""
    root = NOTES[s % len(NOTES)]
    third = root * (1.25 if s % 2 else 1.2)
    fifth = root * 1.5
    tempo = 1.5 + (s % 5) * 0.35  # chord changes per second
    lfo = 0.2 + (s % 7) * 0.1
    fade = f"min(1,t/2)*min(1,({duration}-t)/2)"
    return (
        f"{fade}*0.18*(sin(2*PI*{root}*t*(1+0.25*lt(mod(t*{tempo},4),2)))"
        f"+0.6*sin(2*PI*{third}*t)*(0.5+0.5*sin(2*PI*{lfo}*t))"
        f"+0.4*sin(2*PI*{fifth}*t*(1+0.125*gt(mod(t*{tempo},3),2))))"
    )


def run(cmd):
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        sys.stderr.write(res.stderr)
        raise SystemExit(f"command failed: {' '.join(cmd[:4])}...")


def make_cover(path, colors, s):
    c0, c1 = colors
    run([
        "ffmpeg", "-y", "-loglevel", "error", "-f", "lavfi",
        "-i", f"gradients=s=500x500:c0={c0}:c1={c1}:x0=0:y0=0:x1=500:y1=500:seed={s % 1000}:d=1",
        "-frames:v", "1", path,
    ])


def make_track(path, album, title, number, total, cover, fmt):
    artist = album["artist"]
    track_artist = artist
    if album["type"] == "compilation" and "(" in title:
        title, track_artist = title[:-1].split(" (")
    s = seed(artist, album["album"], title)
    duration = 18 + s % 13
    tags = {
        "title": title,
        "artist": track_artist,
        "album_artist": artist,
        "album": album["album"],
        "track": f"{number}/{total}",
        "disc": "1/1",
        "date": str(album["year"]),
        "genre": album["genre"],
        "publisher": album["label"],
        "ISRC": f"QZ{s % 100:02d}{album['year'] % 100:02d}{s % 100000:05d}",
        "BPM": str(70 + s % 80),
        "RELEASETYPE": album["type"],
    }
    if (artist, title) in MISSING_GENRE:
        del tags["genre"]
    if (artist, title) in MISSING_YEAR:
        del tags["date"]
    if album["genre"] not in NO_LYRICS_GENRES and s % 4 != 0:
        tags["LYRICS"] = LYRICS.format(title=title, word=["rain", "sea", "city", "dawn"][s % 4])
    if album["type"] == "compilation":
        tags["compilation"] = "1"

    if fmt == "flac":
        # Vorbis comments carry the total in its own field; "5/6" would read as track 0.
        tags.update(track=str(number), TRACKTOTAL=str(total), disc="1", DISCTOTAL="1")

    expr = audio_expr(s, duration)
    cmd = [
        "ffmpeg", "-y", "-loglevel", "error",
        "-f", "lavfi", "-i", f"aevalsrc='{expr}|{expr}':s=44100:d={duration}",
        "-i", cover,
    ]
    # Soulsolid estimates FLAC duration from file size at ~1000 kbps, and pure tones
    # compress far below that. A quiet stereo hiss brings the bitrate close to a real
    # recording, so the displayed durations come out right.
    for ch in (1, 2):
        cmd += ["-f", "lavfi", "-i", f"anoisesrc=amplitude=0.02:color=white:seed={s + ch}:sample_rate=44100:duration={duration}"]
    cmd += ["-filter_complex", "[2][3]join=inputs=2:channel_layout=stereo[n];[0][n]amix=inputs=2:normalize=0[a]", "-map", "[a]"]
    cmd += ["-map", "1:v", "-disposition:v", "attached_pic", "-metadata:s:v", "comment=Cover (front)"]
    if fmt == "flac":
        cmd += ["-c:a", "flac", "-sample_fmt", "s16", "-c:v", "mjpeg"]
    else:
        cmd += ["-c:a", "libmp3lame", "-b:a", "128k", "-c:v", "mjpeg", "-id3v2_version", "3"]
    for k, v in tags.items():
        cmd += ["-metadata", f"{k}={v}"]
    run(cmd + [path])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("out")
    ap.add_argument("--dupes")
    args = ap.parse_args()

    with tempfile.TemporaryDirectory() as tmp:
        count = 0
        for album in CATALOG:
            album_dir = os.path.join(args.out, album["artist"], album["album"])
            os.makedirs(album_dir, exist_ok=True)
            cover = os.path.join(tmp, f"{seed(album['album'])}.jpg")
            make_cover(cover, album["colors"], seed(album["album"]))
            total = len(album["tracks"])
            for i, title in enumerate(album["tracks"], 1):
                name = f"{i:02d} {title}.{album['format']}"
                make_track(os.path.join(album_dir, name), album, title, i, total, cover, album["format"])
                count += 1
        print(f"generated {count} tracks in {args.out}")

    if args.dupes:
        # Copies of tracks already in the library, as a downloader might fetch them again:
        # same audio, so same fingerprint, so the importer queues them for manual review.
        picks = [(CATALOG[2], 2), (CATALOG[3], 1), (CATALOG[8], 2)]
        for album, idx in picks:
            title = album["tracks"][idx - 1]
            name = f"{idx:02d} {title}.{album['format']}"
            src = os.path.join(args.out, album["artist"], album["album"], name)
            d = os.path.join(args.dupes, album["artist"])
            os.makedirs(d, exist_ok=True)
            shutil.copy(src, os.path.join(d, f"{album['artist']} - {title}.{album['format']}"))
        print(f"generated {len(picks)} duplicates in {args.dupes}")


if __name__ == "__main__":
    main()
