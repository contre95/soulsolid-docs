---
title: "Soulsolid"
description: "A music library management application with Telegram bot integration"
lead: "Music software for the music hoarder"
date: 2025-10-05T00:00:00+02:00
lastmod: 2025-10-05T00:00:00+02:00
draft: false
seo:
  title: "Soulsolid" # custom title (optional)
  description: "A music library management application with Telegram bot integration" # custom description (recommended)
  canonical: "" # custom canonical URL (optional)
  noindex: false # false (default) or true
---

<table>
  <tr>
    <td><img src="/galaxy.png" width="50" alt="soulsolid"></td>
    <td><h1>Soulsolid</h1></td>
  </tr>
</table>

[![Join Discord](https://img.shields.io/badge/Discord-Join%20Server-5865F2?logo=discord&logoColor=white)](https://discord.gg/mHRjGAjEJz)

A work in progress, feature rich music organization app built for the music hoarder. Heavily under development, focused on ease of usage and start up. Feel free to check the [docs](https://soulsolid.contre.io) or [demo](https://soulsolid-demo.contre.io)

## Features

- **Music Library Management**: Organize and browse albums, artists, and tracks
- **Downloading**: Download tracks and albums.
- **Importing**: Import music from directories with automatic fingerprinting
- **Metadata Tagging**: Auto-tag using MusicBrainz and Discogs APIs
- **Sync with DAP**: Sync library with digital audio players
- **Telegram Integration**: Control via Telegram bot
- **Web UI**: Mobile-friendly interface for all operations
- **Job Management**: Background processing for downloads, imports, and syncs

## Screenshots

<img src="/app-dashboard.jpg" alt="Soulsolid Dashboard" style="max-width: 100%; height: auto; border: 1px solid #ddd; border-radius: 8px; margin: 10px 0;">
<p style="text-align: center; font-style: italic; color: #666;">Main dashboard interface</p>

<img src="/app-library.jpg" alt="Music Library Management" style="max-width: 100%; height: auto; border: 1px solid #ddd; border-radius: 8px; margin: 10px 0;">
<p style="text-align: center; font-style: italic; color: #666;">Library browsing and organization</p>

<img src="/app-settings.jpg" alt="Settings and Configuration" style="max-width: 100%; height: auto; border: 1px solid #ddd; border-radius: 8px; margin: 10px 0;">
<p style="text-align: center; font-style: italic; color: #666;">App configuration options</p>

## Quick Start

### 🦭 Container Usage

The application can run without copying `config.yaml` into the container. If no config file exists, it will automatically create one with sensible defaults.

#### Environment Variable Support

Soulsolid supports environment variables in configuration files using the `!env_var` tag:

```yaml
telegram:
  token: !env_var TELEGRAM_BOT_TOKEN
metadata:
  providers:
    discogs:
      secret: !env_var DISCOGS_API_KEY
```

The application will fail to start if a referenced environment variable is not set.

```bash
# Build the image
podman build -t soulsolid .

# Run with environment variables
podman run -d \
  --name soulsolid \
  -p 3535:3535 \
  -v /host/music:/app/library \
  -v /host/downloads:/app/downloads \
  -v /host/logs:/app/logs \ # optional
  -v /host/library.db:/data/library.db \
  -v /host/config.yaml:/config/config.yaml \
  soulsolid
```

Optionally, to hide secrets, you can use `!env_var` syntax anywhere in your `config.yaml`:

```yaml
telegram:
  token: !env_var TELEGRAM_BOT_TOKEN
metadata:
  providers:
    discogs:
      secret: !env_var DISCOGS_API_KEY
```

The web interface will be available at `http://localhost:3535`.
