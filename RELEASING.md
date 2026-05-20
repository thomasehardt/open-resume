# Releasing

This project uses [Release Please](https://github.com/googleapis/release-please) for automated versioning. Releases publish a versioned Docker image to GHCR.

## The release lifecycle

```
Commit to main → Release Please PR → Merge → GitHub Release → Docker image published
```

## How it works

1. Commit to `main` using conventional commit messages (see below).
2. Release Please scans commits and creates or updates a release PR with the next version number and changelog.
3. Review and merge the release PR.
4. On merge, Release Please creates a GitHub Release with a version tag (e.g. `v1.2.0`).
5. The `docker-publish.yml` workflow builds the Docker image and pushes it to `ghcr.io/thomasehardt/open-resume` tagged with the version and `latest`.
6. The `release.yml` workflow generates example resume files and attaches them to the release (useful for fork users who customize the content).

## Commit message conventions

Release Please determines the next version from your commit messages. Follow [Conventional Commits](https://www.conventionalcommits.org/):

| Prefix | Version bump | Example |
|--------|-------------|---------|
| `feat:` | Minor (1.1.0 → 1.2.0) | `feat: add custom footer support` |
| `fix:` | Patch (1.1.0 → 1.1.1) | `fix: correct page margin in modern theme` |
| `docs:` | None | `docs: update theme creation guide` |
| `chore:` | None | `chore: bump ruff version` |
| `refactor:` | None | `refactor: simplify theme loader` |

Breaking changes use `feat!:` or `fix!:` and bump the major version.

## Performing a release

```bash
# Normal development — just push to main
git add -A && git commit -m "feat: add dark mode theme" && git push

# Release Please will create/update a PR. Merge it when ready.
# The release is automatic from there.
```

## Triggering a release manually

If you need to release without merging a new feature (e.g. to publish the current state):

```bash
git commit --allow-empty -m "chore: release $(git describe --tags)"
git push
```

This creates an empty commit that triggers Release Please to evaluate the release PR.

## What gets published

For each release, the `docker-publish.yml` workflow pushes to `ghcr.io/thomasehardt/open-resume`:

- `:latest` — always points to the latest release
- `:vX.Y.Z` — pinned to the specific version
- `:vX.Y` — major.minor tag

## Forking

If you fork this repo, the same release workflow applies to your fork. Your Docker image will be published to your fork's GHCR namespace automatically (`ghcr.io/<your-username>/open-resume`).
