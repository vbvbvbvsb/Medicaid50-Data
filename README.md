# Medicaid50 Data

A sourced research database of Medicaid casualty and third-party liability (TPL) reporting routes for personal injury (PI) and workers’ compensation (WC), covering all 50 U.S. states and the District of Columbia.

**Version 1.0.1 · Snapshot packaged November 16, 2026 · [ODbL 1.0](LICENSE)**

| Collection | Records |
| --- | ---: |
| Jurisdictions | 51 |
| Managed-care routes | 60 |
| Source records | 436 |
| Portal records | 21 |
| Candidate portals | 4 |
| Practitioner answer sections | 358 |
| Open practitioner questions | 230 |

These counts describe different units. All 51 jurisdictions have an established initial PI route and initial WC route under the dataset’s scoped evidence standard. Some determinations incorporate explicitly attributed practitioner confirmations. This does not establish every plan’s handling, every downstream workflow, or a universal legal clearance. The 60 managed-care records have known contact routes; case-specific follow-through remains necessary.

## Download and use

Download the versioned ZIP from [GitHub Releases](https://github.com/vbvbvbvsb/Medicaid50-Data/releases), or read [the full JSON](data/medicaid_reporting_directory.json). Fresh [CSV exports](data/csv) provide the state directory, field-level evidence, managed-care routes, portal records, source registry, questions and answers. JSON is authoritative; CSV nested values use JSON strings and formula-like text is prefixed with an apostrophe for spreadsheet safety.

```python
import json
from pathlib import Path

directory = json.loads(Path('data/medicaid_reporting_directory.json').read_text())
new_jersey = next(s for s in directory['states'] if s['state_code'] == 'NJ')
print(new_jersey['personal_injury']['initial_reporting_method'])
```

Each fact carries a value, evidence status, source IDs, verification date and scope note. Read those together. Null or unresolved values mean the research has not established the answer. A portal requiring an existing recovery case ID does not establish a new-case reporting route.

## Currency and evidence

November 16 is the snapshot packaging date, not a re-verification date. Use each fact’s `verified_on`, each source’s `reviewed_on`, and the stated document/service dates. Older `metadata.as_of`, edition strings, historical audit records and dated promotion summaries are retained for provenance; use `metadata.public_release` for release identity. External links were not all rechecked for this release.

The snapshot contains canonical bundled research. It does not include the private application, hosted database edits, saved reviews, case files, correspondence attachments, research captures, credentials or the private repository’s history. Six practitioner-evidence source records point to [public provenance notes](docs/source-provenance.md), which distinguish reported practice from independently accessible evidence. These notes do not republish the underlying private materials.

This is research information, not legal advice. Confirm the current recipient, program, claim type, notice/service requirements and secure submission channel before acting. Use the actual case demand for payment instructions. No account creation, notice filing, payment or authenticated transaction is represented by this release.

## License and attribution

The database is made available under the [Open Data Commons Open Database License 1.0](https://opendatacommons.org/licenses/odbl/1-0/). See [LICENSE](LICENSE) and [NOTICE](NOTICE). Attribution, share-alike and access-to-derivative-database provisions apply as specified in that license; commercial use is permitted.

Suggested attribution:

> Contains information from [Medicaid50 Data](https://github.com/vbvbvbvsb/Medicaid50-Data), Possumworks, version 1.0.1 (November 16, 2026), made available under the [Open Database License 1.0](https://opendatacommons.org/licenses/odbl/1-0/).

ODbL licenses the database rights held by the licensor. It does not grant rights in third-party websites, forms, documents, correspondence, trademarks or independently copyrighted contents. Links and references identify evidence; they are not claims that the linked material is ODbL licensed. The small validation/export utilities are separately [MIT licensed](LICENSE-CODE).

## Validate and reproduce exports

Python 3.11 or newer; no third-party packages required. Run without Python’s `-O` flag because the validator uses assertions.

```sh
python3 scripts/release.py --check
python3 scripts/release.py --build
```

`--check` validates the bundled schema, jurisdiction coverage, source references, supported facts, export consistency, basic sensitive-value patterns and checksums. `--build` regenerates exports and creates a deterministic release ZIP and asset checksums under `dist/`. It does not reverify external facts or establish that the data is free of every possible sensitive value.

[GitHub Actions](https://github.com/vbvbvbvsb/Medicaid50-Data/actions/workflows/validate.yml) validates pushes and pull requests, and supports manual runs. It checks the schema, source references, generated CSVs and checksums, then builds the release archive. Pushing a stable version tag also publishes the validated ZIP and asset checksums to GitHub Releases after the tag/version and main-history gates pass; see [release instructions](docs/releasing.md).

See [data dictionary](docs/data-dictionary.md), [methodology](docs/methodology.md), [contribution guidance](CONTRIBUTING.md), [changelog](CHANGELOG.md), and [release instructions](docs/releasing.md). Report corrections with a source, scope and date; do not include client information.
