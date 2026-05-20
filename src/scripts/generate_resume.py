#!/usr/bin/env python3
import os
import sys
import subprocess
import argparse
import yaml
from jinja2 import Environment, FileSystemLoader, select_autoescape
from weasyprint import HTML as WeasyHTML


def load_resume_data(data_file):
    with open(data_file, "r") as f:
        return yaml.safe_load(f)


def render_template(data, template_name, templates_dir):
    env = Environment(
        loader=FileSystemLoader(templates_dir),
        autoescape=select_autoescape(["html", "xml"]),
    )
    template = env.get_template(f"{template_name}.html")
    return template.render(resume=data)


def generate_html(data, output_path, theme, templates_dir, short=False):
    env = Environment(
        loader=FileSystemLoader(templates_dir),
        autoescape=select_autoescape(["html", "xml"]),
    )
    template = env.get_template(f"themes/{theme}.html")
    return template.render(resume=data, short=short)


def generate_pdf(input_html, output_path):
    pdf_doc = WeasyHTML(input_html).write_pdf()
    with open(output_path, "wb") as f:
        f.write(pdf_doc)
    return output_path


def generate_docx(input_html, output_path):
    temp_md = output_path.replace(".docx", ".md")
    with open(input_html, "r") as f:
        html_content = f.read()

    from bs4 import BeautifulSoup

    soup = BeautifulSoup(html_content, "html.parser")

    md_content = ""
    for elem in soup.find_all(
        ["h1", "h2", "h3", "h4", "p", "ul", "ol", "li", "strong", "em"]
    ):
        text = elem.get_text().strip()
        if elem.name == "h1":
            md_content += f"# {text}\n\n"
        elif elem.name == "h2":
            md_content += f"## {text}\n\n"
        elif elem.name == "h3":
            md_content += f"### {text}\n\n"
        elif elem.name == "p":
            md_content += f"{text}\n\n"
        elif elem.name == "ul" or elem.name == "ol":
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
    from bs4 import BeautifulSoup, Tag, NavigableString

    with open(input_html, "r") as f:
        html_content = f.read()

    soup = BeautifulSoup(html_content, "html.parser")

    def is_block_container(tag):
        if tag.name in ("table",):
            return True
        if tag.find(["h1", "h2", "h3", "h4", "p", "ul", "ol", "table"]) is not None:
            return True
        div_count = sum(
            1 for c in tag.children if isinstance(c, Tag) and c.name == "div"
        )
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


def generate_all_versions(data, output_base, templates_dir):
    """Generate specific standardized versions: ATS and Modern."""
    base_name = data.get("name", "resume").lower().replace(" ", "-")
    
    # Configuration for specific standardized outputs
    configs = [
        {"theme": "ats", "is_short": False, "label": "Full (ATS)"},
        {"theme": "modern", "is_short": True, "label": "Short (Handout)"}
    ]

    for config in configs:
        theme = config["theme"]
        is_short = config["is_short"]
        label = config["label"]
        
        theme_dir = os.path.join(output_base, theme)
        os.makedirs(theme_dir, exist_ok=True)

        env = Environment(
            loader=FileSystemLoader(templates_dir),
            autoescape=select_autoescape(["html", "xml"]),
        )
        template = env.get_template(f"themes/{theme}.html")
        html_content = template.render(resume=data, short=is_short)

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
        
        print(f"  {theme}/ generated ({label}).")

    return True


def main():
    parser = argparse.ArgumentParser(description="Generate resume in standardized formats")
    parser.add_argument(
        "-d",
        "--data",
        default="src/content/examples/senior-backend-engineer.yaml",
        help="Path to YAML data file",
    )
    parser.add_argument("-o", "--output", default="output", help="Output directory")

    args = parser.parse_args()

    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.abspath(os.path.join(script_dir, "..", ".."))
    templates_dir = os.path.join(project_root, "src", "templates")
    data_file = (
        args.data if os.path.isabs(args.data) else os.path.join(project_root, args.data)
    )

    if not os.path.exists(data_file):
        print(f"Error: Data file not found: {data_file}")
        return

    data = load_resume_data(data_file)
    output_base = (
        args.output
        if os.path.isabs(args.output)
        else os.path.join(project_root, args.output)
    )

    print("Generating standardized resumes...\n")
    generate_all_versions(data, output_base, templates_dir)

    print(f"\nDone! Generated resume packages in {output_base}/")


if __name__ == "__main__":
    main()
