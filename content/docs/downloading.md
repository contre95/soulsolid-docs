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
      # url: https://github.com/contre95/soulsolid-dummy-plugin # Alternative Git repository URL
      icon: https://demo2.contre.io/img/galaxy.png
      config: {}
  artwork:
    embedded:
      enabled: true
      size: 1000
      quality: 85
```

For a complete configuration example, see the [Configuration](../config/) documentation.

### Git Repository Support

Soulsolid now supports automatic building of plugins directly from Git repositories. Instead of manually building plugins, you can specify a `url` field pointing to a Git repository, and the application will automatically clone, build, and load the plugin.

**Features:**

- **Git Repository Support**: Specify `url: https://github.com/user/repo.git` to automatically build plugins
- **Automatic Build Process**: Clones repository, adds module replacement directive, runs `go mod tidy`, builds with `-buildmode=plugin`
- **Backward Compatibility**: Existing `path` field continues to work for local/HTTP .so files
- **Comprehensive Error Handling**: Clean temporary directories on failure, detailed error logging
- **Module Resolution**: Automatically finds soulsolid module root for proper dependency replacement

**Configuration Example:**

```yaml
downloaders:
  plugins:
    - name: dummy
      url: https://github.com/contre95/soulsolid-dummy-plugin
      # path: /app/plugins/dummy/plugin.so # Can still be used as fallback
      icon: https://demo2.contre.io/img/galaxy.png
      config: {}
```

**Known Limitations & Future Improvements:**

- **No caching**: Plugins rebuild on each application start (just to start simple + Go needs rebuild every version change)
- **Default branch only**: Always clones default branch, no branch/tag/commit support (extend to support old versions)
- **Repository root only**: Assumes plugin is at repository root, no subdirectory support (limits plugin dev but it's ok)
- **Temp file accumulation**: Built .so files remain in /tmp after loading (just limitations)

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
