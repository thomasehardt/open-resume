#!/usr/bin/env python3
"""Generate cover letter from template using resume data."""

import os
import sys
import argparse
from datetime import datetime
from jinja2 import Template
import yaml

DEFAULT_TEMPLATE = "src/templates/cover-letter.md"


def main():
    parser = argparse.ArgumentParser(description="Generate cover letter")
    parser.add_argument(
        "-o", "--output", default="output/cover-letter.md", help="Output file"
    )
    parser.add_argument(
        "-t", "--template", default=DEFAULT_TEMPLATE, help="Template file"
    )
    args = parser.parse_args()

    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.abspath(os.path.join(script_dir, "..", ".."))
    template_file = os.path.join(project_root, args.template)
    data_file = os.path.join(project_root, "src/content/thomas-ehardt.yaml")

    with open(data_file) as f:
        resume = yaml.safe_load(f)

    with open(template_file) as f:
        template = Template(f.read())

    output_path = os.path.join(project_root, args.output)
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    with open(output_path, "w") as f:
        f.write(
            template.render(
                resume=resume, current_date=datetime.now().strftime("%B %d, %Y")
            )
        )

    print(f"Generated: {output_path}")
    print("Edit the bracketed placeholder fields before using.")


if __name__ == "__main__":
    main()
