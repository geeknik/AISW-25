import csv
import importlib.util
import re
import sys
import tempfile
import textwrap
import unittest
from collections import Counter
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = REPO_ROOT / "tools" / "checklist_generator.py"

SPEC = importlib.util.spec_from_file_location("checklist_generator", MODULE_PATH)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError(f"Unable to load checklist generator module from {MODULE_PATH}")

checklist_generator = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = checklist_generator
SPEC.loader.exec_module(checklist_generator)


def build_entry(
    entry_id: str = "AISW-999",
    *,
    severity: str = "HIGH",
    detection_lines: tuple[str, ...] = ("- First check", "- Second check"),
    mitigation_lines: tuple[str, ...] = ("- First mitigation", "- Second mitigation"),
) -> str:
    detection_block = "\n".join(detection_lines)
    mitigation_block = "\n".join(mitigation_lines)
    return (
        f"# {entry_id}: Sample Entry\n\n"
        "| Field | Value |\n"
        "|-------|-------|\n"
        f"| **Identifier** | {entry_id} |\n"
        "| **Rank** | #99 of 25 |\n"
        f"| **Severity** | {severity} |\n\n"
        "---\n\n"
        "## Description\n\n"
        "Sample description.\n\n"
        "## Exploit Scenario\n\n"
        "Sample scenario.\n\n"
        "## Detection Methods\n\n"
        f"{detection_block}\n\n"
        "## Mitigations\n\n"
        f"{mitigation_block}\n\n"
        "## Related Mappings\n\n"
        "- **CWE-20**: Improper Input Validation\n\n"
        "## Severity Rationale\n\n"
        "Sample rationale.\n"
    )


class ChecklistGeneratorTests(unittest.TestCase):
    def test_parse_entry_supports_wrapped_bullet_lines(self) -> None:
        detection_lines = (
            "- First check continues",
            "  onto a wrapped line",
            "- Second check",
        )
        mitigation_lines = (
            "- First mitigation",
            "- Second mitigation continues",
            "  with extra detail",
        )

        with tempfile.TemporaryDirectory() as tmpdir:
            entry_path = Path(tmpdir) / "AISW-999.md"
            entry_path.write_text(
                build_entry(
                    detection_lines=detection_lines,
                    mitigation_lines=mitigation_lines,
                ),
                encoding="utf-8",
            )

            entry = checklist_generator.parse_entry(entry_path)

        self.assertEqual(
            entry.detection,
            ("First check continues onto a wrapped line", "Second check"),
        )
        self.assertEqual(
            entry.mitigations,
            ("First mitigation", "Second mitigation continues with extra detail"),
        )

    def test_load_entries_rejects_missing_required_fields(self) -> None:
        invalid_entry = textwrap.dedent(
            """\
            # AISW-001: Broken Entry

            | Field | Value |
            |-------|-------|
            | **Identifier** | AISW-001 |
            | **Rank** | #1 of 25 |

            ## Detection Methods

            - One check

            ## Mitigations

            - One mitigation
            """
        )

        with tempfile.TemporaryDirectory() as tmpdir:
            entry_path = Path(tmpdir) / "AISW-001.md"
            entry_path.write_text(invalid_entry, encoding="utf-8")

            with self.assertRaises(checklist_generator.EntryParseError) as exc:
                checklist_generator.load_entries(Path(tmpdir))

        self.assertIn("AISW-001.md", str(exc.exception))
        self.assertIn("Severity", str(exc.exception))


class CatalogIntegrityTests(unittest.TestCase):
    def test_readme_severity_distribution_matches_entry_files(self) -> None:
        entries = checklist_generator.load_entries(REPO_ROOT / "entries")
        actual_counts = Counter(entry.severity for entry in entries)

        readme = (REPO_ROOT / "README.md").read_text(encoding="utf-8")
        matches = re.findall(
            r"^\| \*\*(CRITICAL|HIGH|MEDIUM)\*\* \| (\d+) \|",
            readme,
            re.MULTILINE,
        )
        documented_counts = {severity: int(count) for severity, count in matches}

        self.assertEqual(
            documented_counts,
            {
                "CRITICAL": actual_counts["CRITICAL"],
                "HIGH": actual_counts["HIGH"],
                "MEDIUM": actual_counts["MEDIUM"],
            },
        )

    def test_machine_readable_mappings_cover_every_entry(self) -> None:
        entry_ids = {
            entry.entry_id
            for entry in checklist_generator.load_entries(REPO_ROOT / "entries")
        }

        mapped_ids: set[str] = set()
        for mapping_path in (
            REPO_ROOT / "mappings" / "cwe-cross-reference.csv",
            REPO_ROOT / "mappings" / "owasp-cross-reference.csv",
        ):
            with mapping_path.open(encoding="utf-8", newline="") as mapping_file:
                for row in csv.DictReader(mapping_file):
                    mapped_ids.update(
                        aisw_id.strip()
                        for aisw_id in row["aisw_ids"].split(";")
                        if aisw_id.strip()
                    )

        self.assertEqual(entry_ids, mapped_ids)


if __name__ == "__main__":
    unittest.main()
