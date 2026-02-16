---
weight: 20
title: "Self hosted"
description: ""
icon: "article"
date: "2025-09-09T21:10:44+02:00"
lastmod: "2025-09-13T12:00:00+02:00"
draft: false
toc: true
---

## Container Usage

The application can run without copying `config.yaml` into the container. If no config file exists, it will automatically create one with sensible defaults.

### Environment Variable Support

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

Alternatively, you can use the provided `Containerfile` to build a container image for Soulsolid.

Here's an example `compose.yaml` file:

```yaml
version: "3.8"
services:
  soulsolid:
    image: soulsolid:beta
    ports:
      - "3535:3535"
    volumes:
      - ./config.yaml:/config/config.yaml
      - ./library.db:/data/library.db
      - ./logs:/app/logs
     environment:
       # optional
       - TELEGRAM_TOKEN=your_telegram_bot_token_here
    restart: unless-stopped
```

Alternatively, you can use Podman commands or Podman-kube pod YAMLs for deployment.

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: soulsolid
  annotations:
    io.podman.annotations.infra.name: "soulsolid-infra"
   labels:
     app: Soulsolid
     purpose: Music Server
     category: Soulsolid
     language: Go
     content: movies,series,music
spec:
  restartPolicy: OnFailure
  containers:
    - name: soulsolid
      image: contre95/soulsolid:beta
      ports:
        - containerPort: 3535
          hostPort: 3055
      securityContext:
        allowPrivilegeEscalation: false
        capabilities: {}
        privileged: false
        readOnlyRootFilesystem: false
      volumeMounts:
        - mountPath: /config/config.yaml
          name: config
        - mountPath: /music
          name: music
        - mountPath: /downloads
          name: downloads
        - mountPath: /dev
          name: disk-by-uuid
          readOnly: true
  volumes:
    - name: music
      hostPath:
        path: /path/to/soulsolid_music
        type: DirectoryOrCreate
     - name: downloads
       hostPath:
         path: /path/to/soulsolid_downloads
         type: DirectoryOrCreate
    - name: config
      hostPath:
        path: ./config/config.yaml
        type: File
     - name: disk-by-uuid
       hostPath:
         path: /dev
         Type: Directory

```

## Development

To set up the development environment:

### Option 1: Manual Setup

```bash
cp config.example.yaml config.yaml
npm run dev
go run ./src/main.go
```

### Option 2: Using Nix (recommended if you have Nix)

If you have Nix installed, use the provided dev.nix shell:

```bash
# Set up all dependencies (Node.js, Go, etc.) and run the necessary commands
nix-shell dev.nix
# Then, simply run:
go run ./src/main.go
```

The web interface will be available at `http://localhost:3535`.

### Building CSS

### Logs

Application logs are written to stdout/stderr. For more detailed logging, check the job logs in `./logs/jobs/` by default.
