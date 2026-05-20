#!/usr/bin/env python3
import argparse
import os
import subprocess
import sys

import yaml
from jinja2 import Environment, FileSystemLoader, select_autoescape
from weasyprint import HTML

BUILTIN_THEMES_DIR = "src/templates/themes"
BUILTIN_TEMPLATES_DIR = "src/templates"
DEFAULT_DATA = "src/content/examples/senior-backend-engineer.yaml"


def load_resume_data(data_file):
    with open(data_file) as f:
        return yaml.safe_load(f)


def merge_theme_dirs(builtin_dir, custom_dir):
    """Return a list of theme directories, custom first for override priority."""
    dirs = []
    if custom_dir and os.path.isdir(custom_dir):
        dirs.append(custom_dir)
    if os.path.isdir(builtin_dir):
        dirs.append(builtin_dir)
    return dirs


def get_available_themes(theme_dirs):
    themes = {}
    for d in theme_dirs:
        if not os.path.isdir(d):
            continue
        for f in os.listdir(d):
            if f.endswith(".html"):
                name = f[:-5]
                if name not in themes:
                    themes[name] = os.path.join(d, f)
    return themes


def generate_html(data, theme, templates_dir, theme_dirs, short=False):
    env = Environment(
        loader=FileSystemLoader(templates_dir),
        autoescape=select_autoescape(["html", "xml"]),
    )
    loader = FileSystemLoader(theme_dirs)
    template = loader.load(env, f"{theme}.html")
    return template.render(resume=data, short=short)


def generate_pdf(input_html, output_path):
    pdf_doc = HTML(input_html).write_pdf()
    with open(output_path, "wb") as f:
        f.write(pdf_doc)
    return output_path


def generate_docx(input_html, output_path):
    temp_md = output_path.replace(".docx", ".md")
    with open(input_html) as f:
        html_content = f.read()

    from bs4 import BeautifulSoup

    soup = BeautifulSoup(html_content, "html.parser")

    md_content = ""
    for elem in soup.find_all(["h1", "h2", "h3", "h4", "p", "ul", "ol", "li", "strong", "em"]):
        text = elem.get_text().strip()
        if elem.name == "h1":
            md_content += f"# {text}\n\n"
        elif elem.name == "h2":
            md_content += f"## {text}\n\n"
        elif elem.name == "h3":
            md_content += f"### {text}\n\n"
        elif elem.name == "p":
            md_content += f"{text}\n\n"
        elif elem.name in ("ul", "ol"):
            for li in elem.find_all("li"):
                md_content += f"- {li.get_text().strip()}\n"
            md_content += "\n"
        elif elem.name == "li":
            md_content += f"- {text}\n"
        elif elem.name == "strong":
            md_content += f"**{text}**"
        elif elem.name == "em":
            md_content += f"*{text}*"

    with open(temp_md, "w") as f:
        f.write(md_content)

    subprocess.run(["pandoc", temp_md, "-o", output_path], check=True)
    os.remove(temp_md)
    return output_path


def generate_md(input_html, output_path):
    import re

    from bs4 import BeautifulSoup, NavigableString, Tag

    with open(input_html) as f:
        html_content = f.read()

    soup = BeautifulSoup(html_content, "html.parser")

    def is_block_container(tag):
        if tag.name in ("table",):
            return True
        if tag.find(["h1", "h2", "h3", "h4", "p", "ul", "ol", "table"]) is not None:
            return True
        div_count = sum(1 for c in tag.children if isinstance(c, Tag) and c.name == "div")
        return div_count >= 2

    def convert(el):
        if isinstance(el, NavigableString):
            text = str(el)
            text = re.sub(r"\s+", " ", text)
            return text if text.strip() else ""

        if not isinstance(el, Tag):
            return ""

        tag = el.name

        if tag in ("style", "script", "meta", "link", "head", "title"):
            return ""

        children_text = "".join(convert(child) for child in el.children)

        if tag in ("h1", "h2", "h3", "h4"):
            text = children_text.strip()
            return f"\n\n{'#' * int(tag[1])} {text}\n" if text else ""

        elif tag == "p":
            text = children_text.strip()
            return f"\n\n{text}" if text else ""

        elif tag in ("ul",):
            result = ""
            for li in el.find_all("li", recursive=False):
                li_text = convert(li).strip()
                if li_text:
                    result += f"\n- {li_text}"
            return result

        elif tag in ("ol",):
            result = ""
            for i, li in enumerate(el.find_all("li", recursive=False), 1):
                li_text = convert(li).strip()
                if li_text:
                    result += f"\n{i}. {li_text}"
            return result

        elif tag == "li":
            return children_text

        elif tag in ("strong", "b"):
            text = children_text.strip()
            return f"**{text}**" if text else ""

        elif tag in ("em", "i"):
            text = children_text.strip()
            return f"*{text}*" if text else ""

        elif tag == "a":
            text = children_text.strip()
            href = el.get("href", "")
            if href and text and href != text:
                return f"[{text}]({href})"
            return text or href or ""

        elif tag == "br":
            return "\n"

        elif tag in ("div", "span", "section", "header", "main", "article", "nav", "body"):
            parts = []
            for child in el.children:
                child_result = convert(child)
                if child_result:
                    parts.append(child_result)
            sep = "\n" if is_block_container(el) else ""
            return sep.join(parts)

        return children_text

    body = soup.find("body") or soup
    result = convert(body).strip()
    result = re.sub(r"\n{4,}", "\n\n\n", result)
    result = re.sub(r"\n{3,}", "\n\n", result)
    result = re.sub(r"^[ \t]+|[ \t]+$", "", result, flags=re.MULTILINE)

    with open(output_path, "w") as f:
        f.write(result + "\n")

    return output_path


def generate_txt(input_html, output_path):
    subprocess.run(["pandoc", input_html, "-o", output_path], check=True)
    return output_path


def generate_single_theme(data, theme, output_base, templates_dir, theme_dirs, short=False):
    base_name = data.get("name", "resume").lower().replace(" ", "-")

    env = Environment(
        loader=FileSystemLoader(templates_dir),
        autoescape=select_autoescape(["html", "xml"]),
    )
    loader = FileSystemLoader(theme_dirs)
    template = loader.load(env, f"{theme}.html")
    html_content = template.render(resume=data, short=short)

    theme_dir = os.path.join(output_base, theme)
    os.makedirs(theme_dir, exist_ok=True)

    html_file = os.path.join(theme_dir, f"{base_name}.html")
    with open(html_file, "w") as f:
        f.write(html_content)

    pdf_file = os.path.join(theme_dir, f"{base_name}.pdf")
    generate_pdf(html_file, pdf_file)

    docx_file = os.path.join(theme_dir, f"{base_name}.docx")
    generate_docx(html_file, docx_file)

    md_file = os.path.join(theme_dir, f"{base_name}.md")
    generate_md(html_file, md_file)

    txt_file = os.path.join(theme_dir, f"{base_name}.txt")
    generate_txt(html_file, txt_file)

    print(f"  {theme}/ generated.")


def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.abspath(os.path.join(script_dir, "..", ".."))

    parser = argparse.ArgumentParser(description="Generate resume in multiple formats and themes")
    parser.add_argument(
        "-d",
        "--data",
        default=DEFAULT_DATA,
        help="Path to YAML data file",
    )
    parser.add_argument(
        "-o",
        "--output",
        default="output",
        help="Output directory",
    )
    parser.add_argument(
        "-t",
        "--theme",
        action="append",
        dest="themes",
        help="Theme(s) to generate (can be specified multiple times, or comma-separated). Default: all available themes.",
    )
    parser.add_argument(
        "--custom-themes-dir",
        help="Directory with custom theme HTML templates. These override built-in themes of the same name.",
    )
    parser.add_argument(
        "--list-themes",
        action="store_true",
        help="List available themes and exit",
    )
    parser.add_argument(
        "--cover-letter",
        action="store_true",
        help="Also generate a cover letter",
    )
    parser.add_argument(
        "--cover-letter-template",
        default="src/templates/cover-letter.md",
        help="Cover letter template path",
    )

    args = parser.parse_args()

    builtin_themes_dir = os.path.join(project_root, BUILTIN_THEMES_DIR)
    builtin_templates_dir = os.path.join(project_root, BUILTIN_TEMPLATES_DIR)
    custom_themes_dir = args.custom_themes_dir

    if custom_themes_dir and not os.path.isabs(custom_themes_dir):
        custom_themes_dir = os.path.join(project_root, custom_themes_dir)

    theme_dirs = merge_theme_dirs(builtin_themes_dir, custom_themes_dir)
    available = get_available_themes(theme_dirs)

    if args.list_themes:
        print("Available themes:")
        for name in sorted(available.keys()):
            print(f"  {name}")
        return

    data_file = args.data if os.path.isabs(args.data) else os.path.join(project_root, args.data)
    if not os.path.exists(data_file):
        print(f"Error: Data file not found: {data_file}")
        sys.exit(1)

    data = load_resume_data(data_file)

    output_base = (
        args.output if os.path.isabs(args.output) else os.path.join(project_root, args.output)
    )

    themes_to_generate = args.themes
    if themes_to_generate:
        expanded = []
        for t in themes_to_generate:
            expanded.extend([x.strip() for x in t.split(",")])
        themes_to_generate = expanded
    else:
        themes_to_generate = list(available.keys())

    for theme in themes_to_generate:
        if theme not in available:
            print(f"Warning: Theme '{theme}' not found. Skipping.")
            continue
        is_short = theme == "modern"
        generate_single_theme(
            data, theme, output_base, builtin_templates_dir, theme_dirs, short=is_short
        )

    print(f"\nDone! Generated files in {output_base}/")

    if args.cover_letter:
        cover_letter_script = os.path.join(script_dir, "generate_cover_letter.py")
        subprocess.run(
            [
                sys.executable,
                cover_letter_script,
                "-d",
                data_file,
                "-t",
                os.path.join(project_root, args.cover_letter_template),
                "-o",
                os.path.join(output_base, "cover-letter.md"),
            ],
            check=True,
        )


if __name__ == "__main__":
    main()
