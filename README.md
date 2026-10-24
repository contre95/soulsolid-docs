# Soulsolid site

The website for [Soulsolid](https://github.com/contre95/soulsolid):

- **Docs**: [soulsolid-docs.contre.io](https://soulsolid-docs.contre.io), a Hugo ([Doks](https://getdoks.org)) site.
  The pages come from the `docs/` folder of the soulsolid repo; this repo only holds the theme,
  layouts and homepage.
- **Demo**: [soulsolid.contre.io](https://soulsolid.contre.io), a read-only static
  snapshot of a real Soulsolid instance, built by `demo/build.sh`.

Both are built from the latest soulsolid release by `.github/workflows/site.yaml` (on push,
on demand, and daily when a new release is out). The workflow publishes each build as the
single commit of a branch, and git-connected Cloudflare Pages projects deploy those branches
as-is (no build command):

| Branch | Cloudflare Pages project | Domain |
| --- | --- | --- |
| `build/docs` | `soulsolid-docs` | soulsolid-docs.contre.io |
| `build/demo` | `soulsolid-demo` | soulsolid.contre.io (`/docs/*` redirects to the docs) |

## Layout

| Path | What |
| --- | --- |
| `content/` | Homepage, license and privacy pages |
| `layouts/`, `assets/`, `static/`, `config/` | Theme overrides and Hugo config |
| `scripts/fetch-soulsolid.sh` | Puts a soulsolid checkout at `.soulsolid/` (latest release, a given ref, or a local working copy) |
| `scripts/publish-branch.sh` | Force-pushes a built folder as the only commit of a `build/*` branch |
| `demo/` | Demo builder: library generator, seeding, crawler and the browser shim |

`config/_default/module.toml` mounts `.soulsolid/docs` as `content/docs`, and
`layouts/_markup/render-link.html` turns the docs' GitHub-style relative links
(`plugins.md`, `../jobs.md#webhooks`) into site URLs.

## Local development

```sh
npm ci

# Docs against your soulsolid working copy (or omit SOULSOLID_DIR for the latest release)
SOULSOLID_DIR=../soulsolid scripts/fetch-soulsolid.sh
npm run dev  # needs Hugo extended 0.148.x

# Demo (needs go, ffmpeg and fpcalc from chromaprint)
demo/build.sh
cd dist-demo && python3 -m http.server 8000
```

Serve the demo over HTTP (not `file://`): its pages use root-relative paths and HTMX requests.
