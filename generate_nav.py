#!/usr/bin/env python3
"""
Scan docs/ and print the nav: section for mkdocs.yml.
Run after adding new pages:
    python generate_nav.py
Then copy the output into mkdocs.yml nav: block.
"""
import os

FIXED_NAV = [
    ("Home", "index.md"),
    ("Architecture", "architecture.md"),
    ("Principles", "principles.md"),
]

SECTIONS = [
    ("Features", "features"),
    ("Setup", "setup"),
    ("Flows", "flows"),
]

FIXED_TAIL = [
    ("API Reference", "api/README.md"),
    ("Changelog", "changelog.md"),
]

TITLE_MAP = {
    "README.md": "Overview",
    "ai-ml.md": "AI / ML",
    "local-development.md": "Local Development",
    "environment-variables.md": "Environment Variables",
    "docker-compose.md": "Docker Compose",
    "appointment-booking.md": "Appointment Booking",
    "queue-tracking.md": "Queue Tracking",
    "symptom-checker-llm.md": "Symptom Checker (LLM)",
    "medication-adherence.md": "Medication Adherence",
    "rasa-deployment.md": "Rasa — Deploy & Train",
    "admin-panel.md": "Admin Panel",
    "patient-app.md": "Patient App",
}

def file_title(filename: str) -> str:
    if filename in TITLE_MAP:
        return TITLE_MAP[filename]
    return filename.replace(".md", "").replace("-", " ").title()

def section_title(dirname: str) -> str:
    return dirname.replace("-", " ").title()

def scan_section(section_dir: str, rel_prefix: str) -> list:
    base = os.path.join("docs", section_dir)
    files = sorted(f for f in os.listdir(base) if f.endswith(".md"))
    items = []
    # README.md always first as Overview
    if "README.md" in files:
        items.append(f'    - {file_title("README.md")}: {rel_prefix}/README.md')
        files.remove("README.md")
    for f in files:
        items.append(f'    - {file_title(f)}: {rel_prefix}/{f}')
    return items

def main():
    lines = ["nav:"]
    for title, path in FIXED_NAV:
        lines.append(f'  - {title}: {path}')

    for section_name, section_dir in SECTIONS:
        lines.append(f'  - {section_title(section_name)}:')
        lines.extend(scan_section(section_dir, section_dir))

    for title, path in FIXED_TAIL:
        lines.append(f'  - {title}: {path}')

    print("\n".join(lines))

if __name__ == "__main__":
    main()
