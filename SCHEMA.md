# Resume Data Schema

This document defines the YAML data structure consumed by the resume generator. All resume content lives in a single YAML file under `src/content/`.

## Top-Level Structure

```yaml
name:        <string>      # Required. Full name.
title:       <string>      # Required. Professional headline / job title.
location:    <string>      # Required. City, State ZIP format.
phone:       <string>      # Required. Phone number (string, may include + and punctuation).
email:       <string>      # Required. Email address.
linkedin:    <string>      # Required. Full LinkedIn URL.

summary:     <text>        # Required. Professional summary (multi-line, YAML pipe syntax).

skills:      <skill_group[]>  # Required. At least one entry.
employment:  <job[]>         # Required. At least one entry.
education:   <education[]>   # Optional. May be omitted or empty.
```

---

## Fields

### `name`
Full name as it should appear on the resume.

```
name: Jane Doe
```

### `title`
Professional headline. Usually current or most-recent title.

```
title: Senior Data Engineer
```

### `location`
Geographic location. City, state, and ZIP are conventional, but any location string is valid.

```
location: Nashville, TN 37201
```

### `phone`
Phone number. Must be a string (YAML interprets values like `+1.615.555.0100` as strings when quoted).

```
phone: "+1.615.555.0100"
```

### `email`
Email address.

```
email: jane@example.com
```

### `linkedin`
Full LinkedIn profile URL.

```
linkedin: https://linkedin.com/in/jane-doe
```

### `summary`
Multi-line professional summary. Uses YAML pipe (`|`) syntax for literal block scalar.

```
summary: |
  Senior Data Engineer with 10+ years of experience building
  scalable data pipelines and distributed systems. ...
```

**Conventions:**
- First sentence should state role level, years of experience, and primary discipline.
- Subsequent sentences should highlight key differentiators and measurable impact.
- Aim for 3-6 sentences total.

---

## Skills

`skills` is a list of skill groups. Each group has a category name and a list of individual skills.

### `category`
Name of the skill group.

### `skills_list`
List of individual skill strings.

```yaml
skills:
  - category: Data Infrastructure
    skills_list:
      - Apache Spark
      - DuckDB
      - Kubernetes

  - category: Languages
    skills_list:
      - Python
      - Java
      - SQL
```

**Conventions:**
- 2-4 skill groups recommended.
- 3-6 skills per group.
- Skills within a group are rendered as a comma-separated list.
- Use standard capitalization for technology names.

---

## Employment

`employment` is a list of jobs, ordered **most recent first** (reverse chronological).

### `company`
Company name.

### `title`
Job title held at this company.

### `start_date` / `end_date`
Date strings. Convention is abbreviated month + year (e.g., `Aug 2020`). Use `Present` for current position.

```yaml
start_date: Aug 2020
end_date: Present
```

### `description`
Multi-line role description. Summarizes the scope, team size, and primary responsibilities.

```
description: |
  Led the data platform team responsible for ...
```

### `achievements`
List of achievement objects. Each achievement has:

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `text` | string | yes | Full achievement bullet |
| `short` | string | no | Condensed version for space-constrained layouts |

```yaml
achievements:
  - text: Reduced pipeline runtime from 48 hours to 10 minutes by re-architecting the ETL layer.
    short: Reduced pipeline runtime by 99% through ETL re-architecture.
  - text: Mentored a team of 5 junior engineers, increasing team velocity by 20%.
```

**Conventions:**
- Each bullet should be a complete, scannable sentence.
- Lead with action verbs (Architected, Led, Designed, Optimized, etc.).
- Include measurable impact where possible: "Reduced cost by 40%", "Improved throughput by 3x".
- The `short` field should preserve the key metric/outcome while trimming context.
- 3-5 achievements per role is typical.
- Older roles may have fewer achievements.

---

## Education

`education` is a list of education entries.

### `degree`
Full degree name.

### `institution`
Institution name.

```yaml
education:
  - degree: Bachelor of Science (BS) in Computer Science
    institution: University of Example
```

**Conventions:**
- List most recent/highest degree first.
- GPA, honors, or minor can be included inline in the degree string, e.g.: `Bachelor of Science (BS) in Computer Science, Magna Cum Laude`.

---

## Example Minimal File

```yaml
name: Jane Doe
title: Senior Data Engineer
location: Nashville, TN 37201
phone: "+1.615.555.0100"
email: jane@example.com
linkedin: https://linkedin.com/in/jane-doe

summary: |
  Senior Data Engineer with 10+ years of experience building scalable data pipelines
  and distributed systems. Proven track record of modernizing legacy infrastructure and
  reducing operational costs through platform standardization.

skills:
  - category: Data Infrastructure
    skills_list:
      - Apache Spark
      - DuckDB
      - Kubernetes
      - AWS
  - category: Languages
    skills_list:
      - Python
      - Java
      - SQL

employment:
  - company: Example Corp
    title: Senior Data Engineer
    start_date: Jan 2022
    end_date: Present
    description: |
      Lead the data platform team, responsible for architecture, reliability,
      and performance of the company's data infrastructure.
    achievements:
      - text: Migrated legacy Spark pipelines to DuckDB, reducing infrastructure costs by 60% with no loss in throughput.
        short: Reduced infrastructure costs by 60% via DuckDB migration.
      - text: Designed and deployed a real-time data ingestion pipeline processing 10M+ events daily.
        short: Built real-time ingestion pipeline processing 10M+ daily events.

  - company: Startup Inc
    title: Data Engineer
    start_date: Mar 2019
    end_date: Dec 2021
    description: |
      Built and maintained data pipelines supporting analytics and machine learning workloads.
    achievements:
      - text: Architected the ETL framework that reduced data processing time from 12 hours to 45 minutes.
        short: Reduced processing time from 12 hours to 45 minutes.

education:
  - degree: Bachelor of Science (BS) in Computer Science
    institution: University of Example
```

## Templates Reference

Templates access data via the `resume` variable:

| Template Expression | Type | Description |
|-------|------|-------------|
| `resume.name` | string | Full name |
| `resume.title` | string | Professional title |
| `resume.location` | string | Location |
| `resume.phone` | string | Phone |
| `resume.email` | string | Email |
| `resume.linkedin` | string | LinkedIn URL |
| `resume.summary` | string | Summary paragraph |
| `resume.skills` | list | Skill groups |
| `resume.employment` | list | Jobs (reverse chronological) |
| `resume.education` | list | Education entries |

### Achievement object

```jinja2
{% for achievement in job.achievements %}
  {{ achievement.text }}     # Full bullet
  {{ achievement.short }}    # Short bullet (if present)
{% endfor %}
```
