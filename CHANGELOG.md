# Changelog

## 1.0.1 — November 16, 2026

Patch release for automated publishing. Version-tag pushes now validate the tagged snapshot and metadata, build the dataset ZIP/checksums, and publish through a dependent GitHub Actions job. Required branch CI and release-gate tests protect the review and publication paths. Release documentation now follows protected-main pull requests.

Dataset facts, source records, evidence dates, scope qualifications and collection counts are unchanged from v1.0.0. Only release identity and packaging/support files change. External sources were not reverified for this patch.

## 1.0.0 — November 16, 2026

First public database release under ODbL 1.0: 51 jurisdictions, 60 managed-care route records, 436 sources, 21 portals, 358 practitioner answer sections and 230 open questions.

Preserves the current canonical research snapshot, including later managed-care contact corrections and the Louisiana UHC Optum/Katch distinction. Existing-case workflows, plan/program limits, document dates, unresolved questions and practitioner attribution remain explicit.

Public packaging adds release metadata, removes 368 capture-file path fields pointing to undistributed evidence, and replaces 45 occurrences of private-portal evidence URLs with public provenance notes. No source IDs, fact values, verification dates or claim/program qualifications are promoted by packaging. CSVs are regenerated from this JSON rather than copied from historical workbook exports.
