# Resume Generator

A data-driven resume system that separates content from presentation. Write your resume in YAML, generate HTML, PDF, DOCX, TXT, and Markdown in multiple themes.

```yaml
# resume.yaml
name: Jane Doe
title: Senior Data Engineer
location: Nashville, TN 37201
phone: "+1.615.555.0100"
email: jane@example.com
linkedin: https://linkedin.com/in/jane-doe
```

## Usage

### Quick start (recommended)

Place a `resume.yaml` in this directory and run:

```bash
./resume
```

This generates both themes (`ats/` and `modern/`), each in HTML, PDF, DOCX, MD, and TXT in `output/`.

Single theme:

```bash
./resume modern
./resume ats
```

Other commands:

```bash
./resume cover-letter   # generate cover letter
./resume themes         # list available themes
./resume build          # build Docker image locally
./resume clean          # remove output/
./resume help           # show full help
```

Customize via environment variables:

```bash
DATA=my-resume.yaml OUTPUT=dist ./resume
```

### Docker directly

```bash
docker run --rm \
  -v $(pwd)/resume.yaml:/app/resume.yaml \
  -v $(pwd)/output:/app/output \
  ghcr.io/thomasehardt/open-resume \
  -d /app/resume.yaml
```

### Docker Compose

```bash
docker compose up
```

Customize paths in `docker-compose.yml` as needed.

### Custom themes

```bash
# via the script
THEMES_DIR=my-themes ./resume modern

# or via Docker directly
docker run --rm \
  -v $(pwd)/resume.yaml:/app/resume.yaml \
  -v $(pwd)/output:/app/output \
  -v $(pwd)/my-themes:/app/custom/themes \
  ghcr.io/thomasehardt/open-resume \
  -d /app/resume.yaml -t compact
```

See [THEMES.md](THEMES.md) for details on creating custom themes.

---

## Data Format

See [SCHEMA.md](SCHEMA.md) for the full data specification.

Example files are in `src/content/examples/`:

| Role | File |
|------|------|
| Senior Backend Engineer | `senior-backend-engineer.yaml` |
| Data Scientist | `data-scientist.yaml` |
| Product Manager | `product-manager.yaml` |
| Junior Software Engineer | `junior-software-engineer.yaml` |
| DevOps Engineer | `devops-engineer.yaml` |
| Frontend Engineer | `frontend-engineer.yaml` |
| Engineering Manager | `engineering-manager.yaml` |
| Cybersecurity Engineer | `cybersecurity-engineer.yaml` |
| Data Engineer | `data-engineer.yaml` |
| UX Designer | `ux-designer.yaml` |

---

## Two Ways to Use This Project

### 1. Fork and customize

Fork the repository, replace `src/content/examples/*.yaml` with your own resume data, and push. The GitHub Actions workflows will automatically generate resume files and attach them to a GitHub Release on every push to `main` or tag push.

```bash
git tag v1.0.0
git push origin v1.0.0
```

The release workflow produces a GitHub Release with all generated formats attached.

A Docker image is also published to GHCR for your fork automatically via the `docker-publish.yml` workflow.

### 2. Use the Docker image directly

Pull the pre-built image and use it with your own data -- no need to clone or fork.

```bash
docker pull ghcr.io/thomasehardt/open-resume:latest
```

See the [Usage](#usage) section above for examples.

---

## Output

Generated files in `output/`:

```
output/
├── ats/
│   ├── jane-doe.html
│   ├── jane-doe.pdf
│   ├── jane-doe.docx
│   ├── jane-doe.md
│   └── jane-doe.txt
└── modern/
    ├── jane-doe.html
    ├── jane-doe.pdf
    ├── jane-doe.docx
    ├── jane-doe.md
    └── jane-doe.txt
```

Output filenames derive from the `name` field in your YAML data.

---

## Themes

Built-in themes:

- **ats** -- Single-column, ATS-optimized (Arial, minimal styling)
- **modern** -- Two-column, styled for human readers

See [THEMES.md](THEMES.md) for full documentation on creating and using themes.

---

## Development

### Build locally

```bash
docker build -t resume-generator .
```

### Run without Docker (for development)

```bash
pip install jinja2 weasyprint pyyaml beautifulsoup4 markdown
python3 src/scripts/generate_resume.py
```

### Workflows

| Workflow | Trigger | Action |
|----------|---------|--------|
| `docker-publish.yml` | Push to main, tag `v*`, or PR | Builds and publishes Docker image to GHCR |
| `latest.yml` | Push to main (content changes) | Generates resume and updates `latest` release |
| `release.yml` | Any tag push | Generates resume and creates a versioned release |
