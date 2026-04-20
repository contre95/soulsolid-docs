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

Soulsolid can automatically build plugins directly from Git repositories. Specify a `url` field pointing to a Git repository and the application will clone, build, and load the plugin on startup.

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

**How it works:** Soulsolid clones the default branch (depth=1), adds a module replace directive to use the local soulsolid source, runs `go mod tidy`, then builds with `-buildmode=plugin`. Requires `git` and `go` in `PATH`.

**Known limitations:**

- Plugins rebuild on every application start (no caching)
- Only the default branch is cloned — no branch/tag/commit selection
- Repository must have a `go.mod` at the root

## Plugin Interface

Your plugin must implement the `Downloader` interface. The full interface:

```go
type Downloader interface {
    // Search
    SearchAlbums(query string, limit int) ([]music.Album, error)
    SearchTracks(query string, limit int) ([]music.Track, error)
    SearchArtists(query string, limit int) ([]music.Artist, error)
    SearchLinks(query string, limit int) (*LinkResult, error)
    // Navigation
    GetAlbumTracks(albumID string) ([]music.Track, error)
    GetArtistAlbums(artistID string) ([]music.Album, error)
    GetChartTracks(limit int) ([]music.Track, error)
    // Download
    DownloadTrack(trackID string, downloadDir string, progressCallback func(downloaded, total int64)) (*music.Track, error)
    DownloadAlbum(albumID string, downloadDir string, progressCallback func(downloaded, total int64)) ([]*music.Track, error)
    DownloadArtist(artistID string, downloadDir string, progressCallback func(downloaded, total int64)) ([]*music.Track, error)
    DownloadLink(url string, downloadDir string, progressCallback func(downloaded, total int64)) ([]*music.Track, error)
    // Info
    GetUserInfo() *UserInfo
    GetStatus() DownloaderStatus
    Name() string
    Capabilities() DownloaderCapabilities
}
```

`Capabilities()` controls which UI elements are shown for your plugin:

```go
type DownloaderCapabilities struct {
    SupportsSearch       bool // enables track/album search UI
    SupportsArtistSearch bool // enables artist search UI
    SupportsDirectLinks  bool // enables URL/link input UI
    SupportsChartTracks  bool // enables charts section
}
```

Return `ErrMethodNotSupported` from any method your plugin does not implement. For a complete working example see the [dummy plugin](https://github.com/contre95/soulsolid-dummy-plugin).

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
