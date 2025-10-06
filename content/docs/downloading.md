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

### Plugin config

```yaml
plugins:
    - name: "dummy"
      path: "/path/to/plugin.so"
      icon: https://demo2.contre.io/img/galaxy.png
  artwork:
    embedded:
      enabled: true
      size: 1000
      format: jpeg
      quality: 85
    local:
      enabled: true
      size: 1200
      format: jpeg
      template: cover.jpg
```

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
