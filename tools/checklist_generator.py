#!/usr/bin/env python3
"""
AISW-25 Review Checklist Generator

Generates security review checklists from AISW-25 entry files.
Supports filtering by severity, output in markdown or plaintext,
and custom checklist scoping by entry ID.

Usage:
    python checklist_generator.py                          # All entries
    python checklist_generator.py --severity CRITICAL HIGH # Filter by severity
    python checklist_generator.py --entries AISW-001 AISW-007 AISW-010
    python checklist_generator.py --format plain           # Plaintext output
    python checklist_generator.py --output checklist.md    # Write to file
"""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Sequence

VERSION = "0.1"
SEVERITY_ORDER = {"CRITICAL": 0, "HIGH": 1, "MEDIUM": 2}
REQUIRED_SECTIONS = (
    "Description",
    "Exploit Scenario",
    "Detection Methods",
    "Mitigations",
    "Related Mappings",
    "Severity Rationale",
)


class EntryParseError(ValueError):
    """Raised when an AISW entry does not match the expected schema."""


@dataclass(frozen=True)
class Entry:
    """Structured representation of a validated AISW entry."""

    filepath: Path
    entry_id: str
    name: str
    severity: str
    rank: int
    detection: tuple[str, ...]
    mitigations: tuple[str, ...]


def parse_entry(filepath: Path | str) -> Entry:
    """Parse and validate one AISW markdown entry."""
    path = Path(filepath)
    content = path.read_text(encoding="utf-8")

    entry_id, name = parse_title(content)
    table_id = extract_table_field(content, "Identifier")
    if table_id != entry_id:
        raise EntryParseError(
            f"identifier mismatch between title ({entry_id}) and table ({table_id})"
        )
    if path.stem != entry_id:
        raise EntryParseError(
            f"filename stem {path.stem!r} does not match identifier {entry_id!r}"
        )

    rank_text = extract_table_field(content, "Rank")
    rank_match = re.fullmatch(r"#(\d+)(?: of \d+)?", rank_text)
    if rank_match is None:
        raise EntryParseError(f"invalid rank value {rank_text!r}")
    rank = int(rank_match.group(1))

    severity = extract_table_field(content, "Severity").upper()
    if severity not in SEVERITY_ORDER:
        raise EntryParseError(f"unsupported severity {severity!r}")

    sections = split_sections(content)
    missing_sections = [name for name in REQUIRED_SECTIONS if name not in sections]
    if missing_sections:
        raise EntryParseError(
            f"missing required sections: {', '.join(missing_sections)}"
        )

    for section_name in REQUIRED_SECTIONS:
        if not sections[section_name].strip():
            raise EntryParseError(f"section {section_name!r} must not be empty")

    detection = parse_bullet_section(
        sections["Detection Methods"], "Detection Methods"
    )
    mitigations = parse_bullet_section(sections["Mitigations"], "Mitigations")
    parse_bullet_section(sections["Related Mappings"], "Related Mappings")

    return Entry(
        filepath=path,
        entry_id=entry_id,
        name=name,
        severity=severity,
        rank=rank,
        detection=detection,
        mitigations=mitigations,
    )


def parse_title(content: str) -> tuple[str, str]:
    """Extract the entry identifier and name from the markdown title."""
    match = re.search(r"^# (AISW-\d+): (.+)$", content, re.MULTILINE)
    if match is None:
        raise EntryParseError("missing title line '# AISW-XXX: Name'")
    return match.group(1), match.group(2).strip()


def extract_table_field(content: str, field_name: str) -> str:
    """Extract one metadata field from the markdown table."""
    pattern = rf"^\|\s*\*\*{re.escape(field_name)}\*\*\s*\|\s*(.+?)\s*\|$"
    match = re.search(pattern, content, re.MULTILINE)
    if match is None:
        raise EntryParseError(f"missing table field {field_name!r}")
    return match.group(1).strip()


def split_sections(content: str) -> dict[str, str]:
    """Split markdown into named level-two sections."""
    matches = list(re.finditer(r"^## (.+)$", content, re.MULTILINE))
    sections: dict[str, str] = {}

    for index, match in enumerate(matches):
        section_name = match.group(1).strip()
        if section_name in sections:
            raise EntryParseError(f"duplicate section {section_name!r}")

        start = match.end()
        end = matches[index + 1].start() if index + 1 < len(matches) else len(content)
        sections[section_name] = content[start:end].strip()

    return sections


def parse_bullet_section(section_body: str, section_name: str) -> tuple[str, ...]:
    """Parse a markdown bullet list and preserve wrapped bullet lines."""
    items: list[str] = []
    current_item: list[str] | None = None

    for raw_line in section_body.splitlines():
        stripped_line = raw_line.strip()
        if not stripped_line:
            continue

        if raw_line.startswith("- "):
            if current_item is not None:
                items.append(" ".join(current_item).strip())
            bullet_text = raw_line[2:].strip()
            if not bullet_text:
                raise EntryParseError(
                    f"section {section_name!r} contains an empty bullet"
                )
            current_item = [bullet_text]
            continue

        if raw_line.startswith("  ") or raw_line.startswith("\t"):
            if current_item is None:
                raise EntryParseError(
                    f"section {section_name!r} starts with a continuation line"
                )
            current_item.append(stripped_line)
            continue

        raise EntryParseError(
            f"section {section_name!r} contains unsupported line format: {raw_line!r}"
        )

    if current_item is not None:
        items.append(" ".join(current_item).strip())

    if not items:
        raise EntryParseError(f"section {section_name!r} must contain bullet items")

    return tuple(items)


def sort_entries(entries: Sequence[Entry]) -> list[Entry]:
    """Sort entries by severity and then rank."""
    return sorted(
        entries,
        key=lambda entry: (SEVERITY_ORDER[entry.severity], entry.rank),
    )


def generate_markdown_checklist(
    entries: Sequence[Entry], title: str | None = None
) -> str:
    """Generate a markdown-formatted review checklist."""
    lines = [f"# {title}" if title else "# AISW-25 Security Review Checklist", ""]
    lines.append(
        f"Generated from AISW-25 v{VERSION} | {len(entries)} entries | "
        "Aether Systems Labs, Inc."
    )
    lines.extend(["", "---", ""])

    current_severity: str | None = None
    for entry in sort_entries(entries):
        if entry.severity != current_severity:
            current_severity = entry.severity
            lines.extend([f"## {entry.severity}", ""])

        lines.extend([f"### {entry.entry_id}: {entry.name}", ""])
        lines.extend(["**Detection Checks:**", ""])
        lines.extend(f"- [ ] {item}" for item in entry.detection)
        lines.append("")
        lines.extend(["**Mitigation Verification:**", ""])
        lines.extend(f"- [ ] {item}" for item in entry.mitigations)
        lines.append("")

    lines.extend(["---", "", f"*AISW-25 v{VERSION} — CC BY-SA 4.0*"])
    return "\n".join(lines)


def generate_plain_checklist(entries: Sequence[Entry]) -> str:
    """Generate a plaintext checklist."""
    lines = ["AISW-25 SECURITY REVIEW CHECKLIST", "=" * 50, ""]

    current_severity: str | None = None
    for entry in sort_entries(entries):
        if entry.severity != current_severity:
            current_severity = entry.severity
            lines.extend([f"\n[{entry.severity}]", "-" * 40])

        lines.append(f"\n  {entry.entry_id}: {entry.name}")
        lines.append("  Detection:")
        lines.extend(f"    [ ] {item}" for item in entry.detection)
        lines.append("  Mitigations:")
        lines.extend(f"    [ ] {item}" for item in entry.mitigations)

    return "\n".join(lines)


def find_entries_dir(cli_value: str | None) -> Path:
    """Resolve the entries directory relative to the repo before cwd fallback."""
    if cli_value is not None:
        candidate = Path(cli_value).expanduser()
        if candidate.is_dir():
            return candidate.resolve()
        raise FileNotFoundError(candidate)

    script_dir = Path(__file__).resolve().parent
    candidates = (
        script_dir.parent / "entries",
        Path.cwd() / "entries",
        Path.cwd().parent / "entries",
    )
    for candidate in candidates:
        if candidate.is_dir():
            return candidate.resolve()

    raise FileNotFoundError("entries")


def load_entries(entries_dir: Path) -> list[Entry]:
    """Load all entries from disk, rejecting partial or malformed catalogs."""
    entry_files = sorted(entries_dir.glob("AISW-*.md"))
    if not entry_files:
        raise EntryParseError("no entry files found")

    entries: list[Entry] = []
    errors: list[str] = []

    for filepath in entry_files:
        try:
            entries.append(parse_entry(filepath))
        except EntryParseError as exc:
            errors.append(f"{filepath.name}: {exc}")

    if errors:
        raise EntryParseError(
            "failed to parse one or more entries:\n- " + "\n- ".join(errors)
        )

    return entries


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate security review checklists from AISW-25 entries."
    )
    parser.add_argument(
        "--entries-dir",
        default=None,
        help="Path to entries directory (default: repo-relative entries/)",
    )
    parser.add_argument(
        "--severity",
        nargs="+",
        choices=sorted(SEVERITY_ORDER),
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

    try:
        entries_dir = find_entries_dir(args.entries_dir)
    except FileNotFoundError:
        print(
            "Error: entries directory not found. Use --entries-dir to specify.",
            file=sys.stderr,
        )
        sys.exit(1)

    try:
        filtered_entries = load_entries(entries_dir)
    except EntryParseError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)

    if args.severity:
        allowed_severities = set(args.severity)
        filtered_entries = [
            entry for entry in filtered_entries if entry.severity in allowed_severities
        ]
    if args.entries:
        allowed_entries = set(args.entries)
        filtered_entries = [
            entry for entry in filtered_entries if entry.entry_id in allowed_entries
        ]

    if not filtered_entries:
        print("Error: no entries match the specified filters.", file=sys.stderr)
        sys.exit(1)

    if args.format == "markdown":
        output = generate_markdown_checklist(filtered_entries, title=args.title)
    else:
        output = generate_plain_checklist(filtered_entries)

    if args.output:
        Path(args.output).write_text(output, encoding="utf-8")
        print(f"Checklist written to {args.output}", file=sys.stderr)
    else:
        print(output)


if __name__ == "__main__":
    main()
