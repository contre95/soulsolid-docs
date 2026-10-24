#!/usr/bin/env python3
"""Fill a running Soulsolid instance with the generated demo library.

Everything goes through the regular HTTP API, so the jobs, logs and import
queue the demo shows are the real thing.

Usage: seed.py <base_url> <db_path> <music_dir> <dupes_dir>
"""

import json
import sqlite3
import sys
import time
import urllib.parse
import urllib.request

PLAYLISTS = [
    ("Late Night Drive", "Synths and slow beats for empty highways.", ["Synthwave", "Ambient"]),
    ("Sunday Morning", "Coffee, records and nowhere to be.", ["Indie Folk", "Jazz"]),
    ("Workout Mix", "Keep moving.", ["Hip-Hop", "Pop", "Electronic"]),
]


def call(base, method, path, data=None, form=False):
    body, headers = None, {"Accept": "application/json"}
    if data is not None:
        if form:
            body = urllib.parse.urlencode(data).encode()
            headers["Content-Type"] = "application/x-www-form-urlencoded"
        else:
            body = json.dumps(data).encode()
            headers["Content-Type"] = "application/json"
    req = urllib.request.Request(base + path, data=body, method=method, headers=headers)
    with urllib.request.urlopen(req, timeout=60) as r:
        raw = r.read()
    try:
        return json.loads(raw)
    except ValueError:
        return raw.decode()


def wait_job(base, job_id, timeout=600):
    deadline = time.time() + timeout
    while time.time() < deadline:
        job = call(base, "GET", f"/jobs/{job_id}")
        job = job.get("Job", job)
        status = str(job.get("Status", "")).lower()
        if status in ("completed", "failed", "cancelled"):
            print(f"  job {job.get('Name')} {status}: {job.get('Message')}")
            if status != "completed":
                raise SystemExit(f"job {job_id} did not complete")
            return
        time.sleep(1)
    raise SystemExit(f"timed out waiting for job {job_id}")


def run_job(base, method, path, data=None):
    res = call(base, method, path, data)
    wait_job(base, res["job_id"])


def main():
    base, db_path, music_dir, dupes_dir = sys.argv[1:5]

    print("importing library")
    run_job(base, "POST", "/import/directory", {"directoryPath": music_dir})
    print("importing duplicates (these stay in the import queue)")
    run_job(base, "POST", "/import/directory", {"directoryPath": dupes_dir})
    print("calculating metrics")
    run_job(base, "POST", "/jobs/start/calculate_metrics?name=Calculate%20library%20metrics")

    print("creating playlists")
    for name, desc, _ in PLAYLISTS:
        call(base, "POST", "/playlists/", {"name": name, "description": desc}, form=True)
    db = sqlite3.connect(db_path)
    ids = dict(db.execute("SELECT name, id FROM playlists"))
    for name, _, genres in PLAYLISTS:
        marks = ",".join("?" * len(genres))
        tracks = db.execute(
            f"SELECT id FROM tracks WHERE genre IN ({marks}) ORDER BY title LIMIT 12", genres
        ).fetchall()
        for (track_id,) in tracks:
            call(base, "POST", "/playlists/items",
                 {"playlist_id": ids[name], "item_type": "track", "item_id": track_id}, form=True)
    count = db.execute("SELECT COUNT(*) FROM tracks").fetchone()[0]
    print(f"seeded {count} tracks and {len(PLAYLISTS)} playlists")


if __name__ == "__main__":
    main()
