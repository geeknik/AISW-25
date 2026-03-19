#!/usr/bin/env python3
"""
AISW-25 Review Checklist Generator

Generates security review checklists from AISW-25 entry files.
Supports filtering by severity, output in markdown or plaintext,
and custom checklist scoping by entry ID.

Usage:
    python checklist-generator.py                          # All entries
    python checklist-generator.py --severity CRITICAL HIGH # Filter by severity
    python checklist-generator.py --entries AISW-001 AISW-007 AISW-010
    python checklist-generator.py --format plain           # Plaintext output
    python checklist-generator.py --output checklist.md    # Write to file
"""

import argparse
import os
import re
import sys
from pathlib import Path


def parse_entry(filepath: str) -> dict:
    """Parse an AISW entry markdown file into structured data."""
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    entry = {"filepath": filepath}

    # Extract ID and name from title
    title_match = re.search(r"^# (AISW-\d+): (.+)$", content, re.MULTILINE)
    if title_match:
        entry["id"] = title_match.group(1)
        entry["name"] = title_match.group(2)

    # Extract severity from table
    sev_match = re.search(r"\*\*Severity\*\*\s*\|\s*(\w+)", content)
    if sev_match:
        entry["severity"] = sev_match.group(1)

    # Extract rank
    rank_match = re.search(r"\*\*Rank\*\*\s*\|\s*#(\d+)", content)
    if rank_match:
        entry["rank"] = int(rank_match.group(1))

    # Extract detection methods
    detection_section = re.search(
        r"## Detection Methods\n\n((?:- .+\n)+)", content
    )
    if detection_section:
        entry["detection"] = [
            line.lstrip("- ").strip()
            for line in detection_section.group(1).strip().split("\n")
            if line.strip()
        ]
    else:
        entry["detection"] = []

    # Extract mitigations
    mitigation_section = re.search(
        r"## Mitigations\n\n((?:- .+\n)+)", content
    )
    if mitigation_section:
        entry["mitigations"] = [
            line.lstrip("- ").strip()
            for line in mitigation_section.group(1).strip().split("\n")
            if line.strip()
        ]
    else:
        entry["mitigations"] = []

    return entry


def generate_markdown_checklist(entries: list, title: str = None) -> str:
    """Generate a markdown-formatted review checklist."""
    lines = []

    if title:
        lines.append(f"# {title}")
    else:
        lines.append("# AISW-25 Security Review Checklist")

    lines.append("")
    lines.append(
        f"Generated from AISW-25 v0.1 | {len(entries)} entries | "
        f"Aether Systems Labs, Inc."
    )
    lines.append("")
    lines.append("---")
    lines.append("")

    severity_order = {"CRITICAL": 0, "HIGH": 1, "MEDIUM": 2}
    sorted_entries = sorted(
        entries, key=lambda e: (severity_order.get(e.get("severity", ""), 3), e.get("rank", 99))
    )

    current_severity = None
    for entry in sorted_entries:
        sev = entry.get("severity", "UNKNOWN")
        if sev != current_severity:
            current_severity = sev
            lines.append(f"## {sev}")
            lines.append("")

        eid = entry.get("id", "???")
        name = entry.get("name", "Unknown")
        lines.append(f"### {eid}: {name}")
        lines.append("")

        lines.append("**Detection Checks:**")
        lines.append("")
        for d in entry.get("detection", []):
            lines.append(f"- [ ] {d}")
        lines.append("")

        lines.append("**Mitigation Verification:**")
        lines.append("")
        for m in entry.get("mitigations", []):
            lines.append(f"- [ ] {m}")
        lines.append("")

    lines.append("---")
    lines.append("")
    lines.append("*AISW-25 v0.1 — CC BY-SA 4.0*")
    return "\n".join(lines)


def generate_plain_checklist(entries: list) -> str:
    """Generate a plaintext checklist."""
    lines = []
    lines.append("AISW-25 SECURITY REVIEW CHECKLIST")
    lines.append("=" * 50)
    lines.append("")

    severity_order = {"CRITICAL": 0, "HIGH": 1, "MEDIUM": 2}
    sorted_entries = sorted(
        entries, key=lambda e: (severity_order.get(e.get("severity", ""), 3), e.get("rank", 99))
    )

    current_severity = None
    for entry in sorted_entries:
        sev = entry.get("severity", "UNKNOWN")
        if sev != current_severity:
            current_severity = sev
            lines.append(f"\n[{sev}]")
            lines.append("-" * 40)

        eid = entry.get("id", "???")
        name = entry.get("name", "Unknown")
        lines.append(f"\n  {eid}: {name}")

        lines.append("  Detection:")
        for d in entry.get("detection", []):
            lines.append(f"    [ ] {d}")

        lines.append("  Mitigations:")
        for m in entry.get("mitigations", []):
            lines.append(f"    [ ] {m}")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="Generate security review checklists from AISW-25 entries."
    )
    parser.add_argument(
        "--entries-dir",
        default=None,
        help="Path to entries directory (default: ./entries or ../entries)",
    )
    parser.add_argument(
        "--severity",
        nargs="+",
        choices=["CRITICAL", "HIGH", "MEDIUM"],
        help="Filter by severity level(s)",
    )
    parser.add_argument(
        "--entries",
        nargs="+",
        help="Filter by specific entry IDs (e.g., AISW-001 AISW-007)",
    )
    parser.add_argument(
        "--format",
        choices=["markdown", "plain"],
        default="markdown",
        help="Output format (default: markdown)",
    )
    parser.add_argument(
        "--output",
        help="Output file path (default: stdout)",
    )
    parser.add_argument(
        "--title",
        help="Custom checklist title",
    )

    args = parser.parse_args()

    # Find entries directory
    entries_dir = args.entries_dir
    if entries_dir is None:
        for candidate in ["./entries", "../entries", "entries"]:
            if os.path.isdir(candidate):
                entries_dir = candidate
                break

    if entries_dir is None or not os.path.isdir(entries_dir):
        print(
            "Error: entries directory not found. Use --entries-dir to specify.",
            file=sys.stderr,
        )
        sys.exit(1)

    # Parse all entry files
    all_entries = []
    for filepath in sorted(Path(entries_dir).glob("AISW-*.md")):
        try:
            entry = parse_entry(str(filepath))
            all_entries.append(entry)
        except Exception as e:
            print(f"Warning: failed to parse {filepath}: {e}", file=sys.stderr)

    if not all_entries:
        print("Error: no entry files found.", file=sys.stderr)
        sys.exit(1)

    # Apply filters
    filtered = all_entries
    if args.severity:
        filtered = [e for e in filtered if e.get("severity") in args.severity]
    if args.entries:
        filtered = [e for e in filtered if e.get("id") in args.entries]

    if not filtered:
        print("Error: no entries match the specified filters.", file=sys.stderr)
        sys.exit(1)

    # Generate output
    if args.format == "markdown":
        output = generate_markdown_checklist(filtered, title=args.title)
    else:
        output = generate_plain_checklist(filtered)

    # Write output
    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(output)
        print(f"Checklist written to {args.output}", file=sys.stderr)
    else:
        print(output)


if __name__ == "__main__":
    main()
