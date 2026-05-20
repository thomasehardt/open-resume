# Themes

Themes control how resume content is presented. They are Jinja2 HTML templates that receive the parsed YAML data and render it into formatted HTML, which is then converted to PDF, DOCX, TXT, and Markdown.

## Built-in Themes

### `ats`
Single-column, sans-serif layout optimized for Applicant Tracking Systems (ATS). Uses Arial font, minimal styling, standard section headers. Good for job applications where a machine will parse the resume first.

- Font: Arial, 10pt
- Layout: Single column, full width
- Sections: Header, Summary, Professional Experience, Technical Skills, Education
- Achievement behavior: Uses `short` field when `short=True` is passed, otherwise `text`

### `modern`
Two-column, styled layout with sidebar. Uses system fonts, blue accent color, and a tighter font size. Designed for human readers.

- Font: System UI (-apple-system, etc.), 8.8pt
- Layout: Two-column (sidebar: skills + education; main: summary + experience)
- Sections: Header (centered), Sidebar (contact, skills, education), Content (summary, experience)
- Achievement behavior: Truncates to first 3 achievements when `short=True`, uses `short` field when available

## Creating a Custom Theme

### 1. Create an HTML file

Create a `.html` file with Jinja2 template syntax. Place it in a directory (e.g., `./my-themes/compact.html`).

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
    <h1>{{ resume.name }}</h1>
    <p>{{ resume.title }} | {{ resume.location }}</p>

    <h2>Experience</h2>
    {% for job in resume.employment %}
    <div class="job">
        <h3>{{ job.company }}</h3>
        <p>{{ job.title }} | {{ job.start_date }} - {{ job.end_date }}</p>
        <p>{{ job.description }}</p>
        <ul>
        {% for achievement in job.achievements %}
            <li>{{ achievement.text }}</li>
        {% endfor %}
        </ul>
    </div>
    {% endfor %}
</body>
</html>
```

### 2. Use it with Docker

```bash
docker run --rm \
  -v $(pwd)/resume.yaml:/app/resume.yaml \
  -v $(pwd)/output:/app/output \
  -v $(pwd)/my-themes:/app/custom/themes \
  ghcr.io/open-resume/resume-generator \
  -d /app/resume.yaml \
  -o /app/output \
  -t compact
```

Custom themes override built-in themes of the same name.

### 3. Use it with docker-compose

```yaml
services:
  resume-generator:
    image: ghcr.io/open-resume/resume-generator
    volumes:
      - ./resume.yaml:/app/resume.yaml
      - ./output:/app/output
      - ./my-themes:/app/custom/themes
    command: -d /app/resume.yaml -o /app/output -t compact
```

## Template Variables

The template receives these variables:

| Variable | Type | Description |
|----------|------|-------------|
| `resume.name` | string | Full name |
| `resume.title` | string | Professional headline |
| `resume.location` | string | Geographic location |
| `resume.phone` | string | Phone number |
| `resume.email` | string | Email address |
| `resume.linkedin` | string | LinkedIn URL |
| `resume.summary` | string | Professional summary |
| `resume.skills` | list | Skill groups (see below) |
| `resume.employment` | list | Work history (see below) |
| `resume.education` | list | Education entries |
| `short` | bool | True when generating a condensed version |

### Skills Structure

```jinja2
{% for group in resume.skills %}
  {{ group.category }}         # "Data Infrastructure"
  {% for skill in group.skills_list %}
    {{ skill }}                # "Apache Spark"
  {% endfor %}
{% endfor %}
```

### Employment Structure

```jinja2
{% for job in resume.employment %}
  {{ job.company }}            # Company name
  {{ job.title }}              # Job title
  {{ job.start_date }}         # Start date string
  {{ job.end_date }}           # End date string ("Present")
  {{ job.description }}        # Role description (multi-line)
  {% for achievement in job.achievements %}
    {{ achievement.text }}     # Full bullet text
    {{ achievement.short }}    # Short version (optional)
  {% endfor %}
{% endfor %}
```

### Education Structure

```jinja2
{% for edu in resume.education %}
  {{ edu.degree }}             # "Bachelor of Science (BS) in CS"
  {{ edu.institution }}        # "University of ..."
{% endfor %}
```

## Theme Recommendations

- **ATS compatibility**: Single column, no headers/footers with critical content, standard fonts (Arial, Times New Roman), 10-12pt font size, no multi-column layouts.
- **Human review**: Two-column layouts are acceptable. Use visual hierarchy, color accents, and whitespace. Stay concise -- a senior engineer should aim for 1-2 pages.
- **Print output**: Use `@page` CSS rules to set print margins. WeasyPrint (the PDF renderer) supports most modern CSS but not all features -- test your theme by generating a PDF.
