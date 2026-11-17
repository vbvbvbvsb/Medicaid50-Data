# Data dictionary

The complete structured database is `data/medicaid_reporting_directory.json`. Its bundled JSON Schema validates the original core directory and route audit structures; later workflow extensions also receive source-reference and release-specific integrity checks. The schema does not exhaustively constrain every later extension.

| Top-level field | Meaning |
| --- | --- |
| `metadata` | Research title, legacy edition/as-of date, evidence definitions, coverage and methodology. `public_release` identifies this distribution and license. |
| `states` | 51 state/DC records, with identification, administration, PI, WC, workflow, clarification contact, issues, notes and verification summaries. |
| `managed_care_routes` | 60 plan/program contacts and routes; read route purpose, claim type and service-date limits. |
| `portal_directory` | 21 established portal records; login and existing-case restrictions remain meaningful. |
| `candidate_portals` | Four candidates; presence does not establish an approved filing route. |
| `verification_queue` | 51 jurisdiction summaries of remaining work, with evidence and historical audit references. |
| `sources` | 436 records keyed by stable `source_id`; title, URL, source type, review date and access observation. Optional capture hashes refer to omitted evidence. |
| `vendor_matrix` | 12 vendor/program relationship summaries; an award or vendor name alone is not a filing route. |
| `route_verification` | Historical qualified/held routes, scoped manual confirmations and operational resolutions. Historical counts are not current question counts. |
| `practitioner_workflows` | Per-state answers, open questions, checklist/research distinctions, common guidance and dated review lineage. |
| `mco_contact_work` | Known contacts, contact-research state and case-level follow-through distinctions. |

A state fact is an object with `value` (text or null), `status`, `source_ids` (registry keys), `verified_on` (date or null) and `note` (scope/evidence caveat). `states[].verification` summarizes independent PI and WC initial-route statuses. Codes use two-letter state abbreviations plus DC. Dates use ISO calendar dates; they describe the particular observation, not continuous accuracy.

CSV exports are regenerated from the JSON. `states.csv` retains nested sections as JSON-valued cells; `field_level_evidence.csv` supplies one state/fact per row. `practitioner_answers.csv` and `practitioner_questions.csv` are flattened convenience views. Arrays and objects are serialized as JSON in a cell; null becomes an empty cell. An initial apostrophe protects formula-like text in spreadsheets; use the JSON for lossless programmatic values. CSVs are UTF-8 with CRLF row separators.

`provenance.json` identifies input selection and public transformations. `validation.json` records machine checks without asserting external-source revalidation. `SHA256SUMS` covers all repository payload files except itself, `.git`, caches and generated `dist/` assets; the release has a separate asset checksum file.
