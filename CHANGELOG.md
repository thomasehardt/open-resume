# Changelog

## [1.0.1](https://github.com/thomasehardt/open-resume/compare/v1.0.0...v1.0.1) (2026-05-20)


### Bug Fixes

* mount data file directly instead of overriding src/ in workflows ([4f194b7](https://github.com/thomasehardt/open-resume/commit/4f194b7322928d6754a2dede8b75041b56a9569e))

## 1.0.0 (2026-05-20)

### Features

* YAML-driven resume content with Jinja2 HTML themes
* Generate HTML, PDF, DOCX, Markdown, and TXT output
* Two built-in themes: ATS-optimized and modern two-column
* Docker-first workflow with `./resume` CLI script
* 10 example resumes for different roles and experience levels
* Custom themes support via `--custom-themes-dir`
* Cover letter generation
* Release Please automated versioning with Conventional Commits
* Docker image publishing to GHCR on releases
* Automatic resume generation on releases and main branch pushes
* Code formatting and linting with ruff
