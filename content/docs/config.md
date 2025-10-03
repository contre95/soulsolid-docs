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
- **downloaders**: External service configurations (Deezer, etc.)

**Security Note**: Never commit sensitive values like tokens or API keys to version control. Use environment variables instead.

### Automatic Configuration

If no `config.yaml` file exists when the application starts, it will automatically create one with sensible default values. This means you can run Soulsolid out of the box without any configuration!

### Default Configuration Values

When auto-generated, the config file includes these defaults:

| Setting               | Default Value  | Description                                          |
| --------------------- | -------------- | ---------------------------------------------------- |
| **Library Path**      | `./music`      | Where your music library is stored                   |
| **Download Path**     | `./downloads`  | Where downloaded music is saved                      |
| **Database Path**     | `./library.db` | SQLite database location                             |
| **Jobs Log Path**     | `./logs/jobs`  | Where job logs are stored                            |
| **Server Port**       | `3535`         | Web interface port                                   |
| **Logger Level**      | `info`         | Logging verbosity (debug, info, warn, error)         |
| **Logger Format**     | `text`         | Log output format (text, json)                       |
| **Import Move**       | `false`        | Whether to move files during import (vs copy)        |
| **Import Duplicates** | `queue`        | How to handle duplicate files (replace, skip, queue) |
| **Jobs Log**          | `true`         | Enable job logging                                   |
| **Artwork Embedded**  | `true`         | Embed album artwork in audio files                   |
| **Artwork Size**      | `1000px`       | Embedded artwork size                                |
| **Artwork Quality**   | `85%`          | JPEG quality for embedded artwork                    |

### Environment Variables

#### Available Environment Variables

| Variable         | Description        | Default |
| ---------------- | ------------------ | ------- |
| `TELEGRAM_TOKEN` | Telegram bot token | -       |
| `DEEZER_ARL`     | Deezer ARL token   | -       |

For security, sensitive values should be set via environment variables rather than stored in config.yaml:

```bash
# Required for Telegram bot functionality
export TELEGRAM_TOKEN="your_telegram_bot_token_here"
# Optional: Deezer downloader
export DEEZER_ARL="your_deezer_arl_token"
```
