---
weight: 50
title: "Configuration"
description: ""
icon: "article"
date: "2025-09-09T21:10:30+02:00"
lastmod: "2025-09-09T21:10:30+02:00"
draft: false
toc: true
---

The `config.yaml` file contains all application settings. Key sections:

- **telegram**: Bot configuration and allowed users
- **library**: Path to your music library
- **import**: Import settings and file organization rules
- **sync**: Device synchronization configuration
- **tag**: Metadata provider settings (Not implemented yet)
- **server**: Web server configuration
- **downloaders**: External service configurations in the form of plugins. Supports both local `.so` files and automatic building from Git repositories.

**Security Note**: Never commit sensitive values like tokens or API keys to version control. Use environment variables instead.

### Automatic Configuration

If no `config.yaml` file exists when the application starts, it will automatically create one with sensible default values. This means you can run Soulsolid out of the box without any configuration!

### Default Configuration Values

When auto-generated, the config file includes these defaults:

```yaml
# Soulsolid Configuration Example
#
# Environment variables can be referenced using the !env_var tag:
#   token: !env_var TELEGRAM_BOT_TOKEN
#
# The application will fail to start if a referenced environment variable is not set.

libraryPath: ./music
downloadPath: ./downloads
telegram:
  enabled: false
  token: !env_var TELEGRAM_BOT_TOKEN
  allowedUsers:
    - <your telegram username>
  bot_handle: SoulsolidExampleBot # Without the @
logger:
  enabled: true
  level: info
  format: text
  htmx_debug: false
downloaders:
  plugins:
    - name: dummy
      path: ../soulsolid-dummy-plugin/plugin.so
      # url: https://github.com/contre95/soulsolid-dummy-plugin # Alternative Git repository URL
      icon: https://demo2.contre.io/img/galaxy.png
      config: {} # Plugin specific config. See https://git.sr.ht/~canuslector/soulsolid-deemix-plugin
  artwork:
    embedded:
      enabled: true
      size: 1000
      quality: 85
server:
  show_routes: false
  port: 3535
database:
  path: ./library.db # Path to the SQLite Database
import:
  move: false # If false tracks will be kepts in the folder where you are importing them from and copied from it to your 'libraryPath:'
  always_queue: false # When true, it will queue every single imported track for manual review.
  duplicates: queue # queue | skip | replace
  allow_missing_metadata: false # When true, allows importing tracks without artist or album metadata
  paths:
    compilations: "%asciify{$albumartist}/%asciify{$album} (%if{$original_year,$original_year,$year})/%asciify{$track $title}"
    album:soundtrack: "%asciify{$albumartist}/%asciify{$album} [OST] (%if{$original_year,$original_year,$year})/%asciify{$track $title}"
    album:single: "%asciify{$albumartist}/%asciify{$album} [Single] (%if{$original_year,$original_year,$year})/%asciify{$track $title}"
    album:ep: "%asciify{$albumartist}/%asciify{$album} [EP] (%if{$original_year,$original_year,$year})/%asciify{$track $title}"
    default_path: "%asciify{$albumartist}/%asciify{$album} (%if{$original_year,$original_year,$year})/%asciify{$track $title}"
  auto_start_watcher: false
metadata:
  providers:
    acoustid:
      enabled: true
      secret: !env_var ACOUSTID_CLIENT_KEY # You can login with Musicbrainz -> https://acoustid.org/new-application
    deezer:
      enabled: true
    discogs:
      enabled: true
      secret: !env_var DISCOGS_API_KEY # You can get it here -> https://www.discogs.com/settings/developers
    musicbrainz:
      enabled: true
lyrics:
  providers:
    lrclib:
      enabled: true
      prefer_synced: false # Some programs like navidrome require synced lyrics
sync:
  enabled: true
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
    command: "echo hi"
```

### Environment Variables

#### Available Environment Variables

These environment variables can be referenced in the configuration file using the `!env_var` tag (e.g., `token: !env_var TELEGRAM_BOT_TOKEN`).

| Variable              | Description                                        | Default |
| --------------------- | -------------------------------------------------- | ------- |
| `TELEGRAM_BOT_TOKEN`  | Overrides the Telegram bot token                   | -       |
| `DISCOGS_API_KEY`     | Sets the Discogs API key for metadata provider     | -       |
| `ACOUSTID_CLIENT_KEY` | Sets the AcoustID client key for metadata provider | -       |
| `IMAGE_TAG`           | Sets the application version                       | dev     |

For security, sensitive values should be set via environment variables rather than stored in config.yaml:

```bash
# Required for Telegram bot functionality
export TELEGRAM_BOT_TOKEN="your_telegram_bot_token_here"
```
