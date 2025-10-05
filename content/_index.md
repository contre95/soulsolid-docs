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

# 🎧 Soulsolid

A music library management application with Telegram bot integration.

## Features

- Music library management and organization
- Telegram bot for remote control and notifications
- Automatic music importing from directories
- Device synchronization (iPod, USB drives, DAP etc.)
- [WIP] Metadata tagging with multiple providers (AcoustID, Discogs, MusicBrainz)
- Web interface for library browsing and management
- Job queue system for background processing

## Screenshots

<img src="/app-dashboard.png" alt="Soulsolid Dashboard" style="max-width: 100%; height: auto; border: 1px solid #ddd; border-radius: 8px; margin: 10px 0;">
<p style="text-align: center; font-style: italic; color: #666;">Main dashboard interface</p>

<img src="/app-library.png" alt="Music Library Management" style="max-width: 100%; height: auto; border: 1px solid #ddd; border-radius: 8px; margin: 10px 0;">
<p style="text-align: center; font-style: italic; color: #666;">Library browsing and organization</p>

<img src="/app-telegram.png" alt="Telegram Bot Integration" style="max-width: 100%; height: auto; border: 1px solid #ddd; border-radius: 8px; margin: 10px 0;">
<p style="text-align: center; font-style: italic; color: #666;">Remote control via Telegram</p>

<img src="/app-settings.png" alt="Settings and Configuration" style="max-width: 100%; height: auto; border: 1px solid #ddd; border-radius: 8px; margin: 10px 0;">
<p style="text-align: center; font-style: italic; color: #666;">App configuration options</p>

## Quick Start

### Docker Usage

The application can run without copying `config.yaml` into the container. If no config file exists, it will automatically create one with sensible defaults. Use environment variables to override specific settings:

```bash
# Build the image
podman build -t soulsolid .

# Run with environment variables (config.yaml will be auto-created if missing)
podman run -d \
  --name soulsolid \
  -p 3535:3535 \
  -v /host/music:/app/library \
  -v /host/downloads:/app/downloads \
  -v /host/logs:/app/logs \
  -v /host/library.db:/app/library.db \
  -v /host/config.yaml:/app/config.yaml \
  -e TELEGRAM_TOKEN="your_token" \
  -e DEEZER_ARL="your_arl" \
  soulsolid
```

The web interface will be available at `http://localhost:3535`.
