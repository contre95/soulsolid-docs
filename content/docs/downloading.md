---
weight: 60
title: "Downloading"
description: ""
icon: "article"
date: "2025-09-09T21:10:28+02:00"
lastmod: "2025-09-09T21:10:28+02:00"
draft: false
toc: true
---

The soulsolid application downloads tracks via configurable plugins and writes metadata tags to the files through a multi-step process. Metadata is fetched from configured providers.

## Installing Plugins

Soulsolid supports downloading music through plugins. To install a plugin, you can build it directly in your Docker container or compile it separately.

### Building a Plugin in Docker

You can extend the Soulsolid Docker image to include custom plugins. Here's an example Dockerfile snippet:

```dockerfile
FROM contre95/soulsolid:nightly
RUN git clone https://github.com/contre95/soulsolid-dummy-plugin /tmp/plugin
WORKDIR /tmp/plugin
RUN go mod edit -replace=github.com/contre95/soulsolid=/app
RUN go mod tidy
RUN go build -buildmode=plugin -o /app/plugins/dummy/plugin.so .
WORKDIR /app
```

This clones the dummy plugin repository, replaces the module path to point to the local Soulsolid code, tidies the modules, builds the plugin as a shared object, and places it in the plugins directory.

### Plugin Configuration

Plugins are configured under the `downloaders` section. Here's an example configuration:

```yaml
downloaders:
  plugins:
    - name: dummy
      path: ../soulsolid-dummy-plugin/plugin.so
      icon: https://soulsolid-demo.contre.io/img/galaxy.png
      config: {}
  artwork:
    embedded:
      enabled: true
      size: 1000
      quality: 85
```

For a complete configuration example, see below.

## Downloading Process

1. Authentication: Uses authentication tokens to access provider APIs
2. Metadata Retrieval: Fetches track metadata from configured providers
3. Audio Download: Downloads audio data via configured plugins
4. Decryption: Decrypts audio data if required by the plugin
5. Format Detection: Automatically detects audio format (MP3, FLAC, etc.) from the decrypted data

## Tagging Process

After downloading, the application embeds comprehensive metadata into the audio files:

### For MP3 files (ID3v2 tags):

• Title, Artist, Album, Year, Genre
• Track/Position in set, Disc number
• ISRC, BPM, ReplayGain
• Album art (from metadata providers)
• Publisher, Barcode, Composer, Lyrics

### For FLAC files (Vorbis comments):

• Similar metadata fields as MP3
• Additional Vorbis-specific fields like VERSION, DISCNUMBER

## Complete Configuration Example

Here's a complete `config.yaml` example including plugin configuration:

```yaml
libraryPath: ./music
downloadPath: ./downloads
telegram:
  enabled: true
  token: <telegram_bot_token>
  allowedUsers:
    - username
  bot_handle: SoulsolidExampleBot
logger:
  enabled: true
  level: info
  format: text
  htmx_debug: false
downloaders:
  plugins:
    - name: dummy
      path: ../soulsolid-dummy-plugin/plugin.so
      icon: https://soulsolid-demo.contre.io/img/galaxy.png
      config: {}
  artwork:
    embedded:
      enabled: true
      size: 1000
      quality: 85
  tag_file: true
server:
  show_routes: false
  port: 3535
database:
  path: ./library.db
import:
  move: false
  always_queue: false
  duplicates: queue
  paths:
    compilations: "%asciify{$albumartist}/%asciify{$album} (%if{$original_year,$original_year,$year})/%asciify{$track $title}"
    album:soundtrack: "%asciify{$albumartist}/%asciify{$album} [OST] (%if{$original_year,$original_year,$year})/%asciify{$track $title}"
    album:single: "%asciify{$albumartist}/%asciify{$album} [Single] (%if{$original_year,$original_year,$year})/%asciify{$track $title}"
    album:ep: "%asciify{$albumartist}/%asciify{$album} [EP] (%if{$original_year,$original_year,$year})/%asciify{$track $title}"
    default_path: "%asciify{$albumartist}/%asciify{$album} (%if{$original_year,$original_year,$year})/%asciify{$track $title}"
metadata:
  providers:
    deezer:
      enabled: true
    discogs:
      enabled: true
      api_key: <discogs_token>
    musicbrainz:
      enabled: true
sync:
  enabled: false
  devices:
    - uuid: 8722-177E
      name: iPod
      sync_path: Soulsolid
jobs:
  log: true
  log_path: ./logs/jobs
  webhooks:
    enabled: true
    job_types:
      - directory_import
      - download_album
      - dap_sync
    command: "TEXT=\"\U0001F3B5 Job {{.Name}} ({{.Type}}) {{.Status}}\\n\U0001F4DD {{.Message}}\\n⏱️ Duration: {{.Duration}}\"\ncurl -X POST -H 'Content-Type: application/json' \\\n  -d '{\"chat_id\": \"<chat_id>\", \"text\": \"'\"$TEXT\"'\", \"parse_mode\": \"HTML\"}' \\\n  https://api.telegram.org/bot<bot_token>/sendMessage\n"
```
