# Resume Generator

A data-driven resume system that separates content from presentation, allowing multiple themes and formats.

## Quick Start

### Generate all formats with default theme:
```bash
docker run --rm -v $(pwd):/app resume-generator
```

### Generate with specific theme:
```bash
docker run --rm -v $(pwd):/app resume-generator -t compact
```

### List available themes:
```bash
docker run --rm -v $(pwd):/app resume-generator --list-themes
```

## Data Format

Resume data lives in YAML files under `src/content/`. See `src/content/examples/` for ready-to-use samples covering various roles and experience levels.

```yaml
name: Your Name
title: Software Engineer
location: City, State ZIP
phone: "+1.555.555.0100"
email: you@example.com
linkedin: https://linkedin.com/in/your-profile

summary: |
  Your professional summary text here.

skills:
  - category: Category Name
    skills_list:
      - Skill One
      - Skill Two

employment:
  - company: Company Name
    title: Job Title
    start_date: Aug 2020
    end_date: Present
    description: |
      Role description.
    achievements:
      - text: Full achievement bullet.
        short: Optional shorter version.
      - text: Another achievement.

education:
  - degree: Degree Name
    institution: University Name
```

### YAML Notes

- Multi-line text uses `|` followed by indented content
- Use `skills_list` (not `items`) for skill lists
- Achievements use objects with required `text` and optional `short` fields
- Dates can be actual dates or strings like "Present" or "Aug 2020"

## Themes

Themes are HTML+Jinja2 templates in `src/templates/themes/`.

### Available Themes

- **full**: Full-length resume (similar to original AsciiDoc version)
- **compact**: Modern 1-page version with two-column layout

### Creating a New Theme

1. Create a new file in `src/templates/themes/`, e.g., `modern.html`:

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>{{ resume.name }} - {{ resume.title }}</title>
    <style>
        /* Your CSS here */
    </style>
</head>
<body>
    <!-- Access resume data via {{ resume.field_name }} -->
    <h1>{{ resume.name }}</h1>
    <p>{{ resume.title }}</p>
    
    <!-- Loops work as expected -->
    {% for job in resume.employment %}
    <h2>{{ job.company }}</h2>
    <p>{{ job.title }} | {{ job.start_date }} - {{ job.end_date }}</p>
    {% endfor %}
</body>
</html>
```

2. Generate with your theme:
```bash
docker run --rm -v $(pwd):/app resume-generator -t modern
```

### Template Variables

| Variable | Description |
|---------|-------------|
| `resume.name` | Full name |
| `resume.title` | Job title |
| `resume.location` | Location |
| `resume.phone` | Phone number |
| `resume.email` | Email address |
| `resume.linkedin` | LinkedIn URL |
| `resume.summary` | Summary text |
| `resume.skills` | List of skill groups |
| `resume.employment` | List of jobs |
| `resume.education` | List of education |

### Skills Structure

```jinja2
{% for skill_group in resume.skills %}
  {{ skill_group.category }}       # e.g., "Cloud & Distributed Systems"
  {% for skill in skill_group.skills_list %}
    - {{ skill }}                  # e.g., "AWS", "GCP"
  {% endfor %}
{% endfor %}
```

### Employment Structure

```jinja2
{% for job in resume.employment %}
  {{ job.company }}
  {{ job.title }}
  {{ job.start_date }} - {{ job.end_date }}
  {{ job.description }}
  {% for achievement in job.achievements %}
    - {{ achievement }}
  {% endfor %}
{% endfor %}
```

## Output Formats

Generated files (in `output/`):
- `<name>-<theme>.html` - HTML
- `<name>-<theme>.pdf` - PDF (via WeasyPrint)
- `<name>-<theme>.docx` - Word (via Pandoc)
- `<name>-<theme>.txt` - Plain text

Output filenames are derived from the `name` field in your YAML data file.

## Development

### Build Docker image:
```bash
./build.sh
```

### Run locally without Docker:
```bash
pip install jinja2 weasyprint pyyaml beautifulsoup4 markdown
python3 src/scripts/generate_resume.py
```

### Test a specific theme:
```bash
python3 src/scripts/generate_resume.py -t compact
```