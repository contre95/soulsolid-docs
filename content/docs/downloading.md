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

The soulsolid application downloads tracks from Deezer and writes metadata tags to the files through a multi-step process.

### Deezer config

```yaml
downloaders:
  deezer:
    enabled: true
    arl: <ARL>
    preferred_quality: FLAC
    fallback_quality: MP3_320
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

1. Authentication: Uses an ARL (authentication token) to access Deezer's private API
2. Metadata Retrieval: Fetches track metadata from Deezer's public API endpoints
3. Audio Download: Downloads encrypted audio data from Deezer's media servers using their private API
4. Decryption: Decrypts the audio data using Blowfish CBC encryption (compatible with streamrip algorithm)
5. Format Detection: Automatically detects audio format (MP3, FLAC, etc.) from the decrypted data

## Tagging Process

After downloading, the application embeds comprehensive metadata into the audio files:

### For MP3 files (ID3v2 tags):

• Title, Artist, Album, Year, Genre
• Track/Position in set, Disc number
• ISRC, BPM, ReplayGain
• Album art (downloaded from Deezer)
• Publisher, Barcode, Composer, Lyrics

### For FLAC files (Vorbis comments):

• Similar metadata fields as MP3
• Additional Vorbis-specific fields like VERSION, DISCNUMBER
