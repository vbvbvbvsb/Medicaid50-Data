# Methodology and limitations

The public snapshot is derived from the canonical research JSON, not historical CSVs, numbered archive folders or the private application’s runtime database. `provenance.json` records the input SHA-256 and source revision. The packaging process adds `metadata.public_release`, replaces private evidence links, removes unavailable capture paths, and regenerates CSVs. It does not change the underlying fact values or statuses.

The directory separates PI and WC, initial notification and downstream actions, state-program and plan-specific routes, official instructions and explicitly attributed practitioner confirmations. Primary agency and identified contractor sources are preferred. Historical and limited-scope material is retained with qualifications; absence of a verified answer is not evidence of no requirement.

Evidence statuses are defined in `metadata.status_definitions`. VERIFIED — PRIMARY and VERIFIED — CONTRACTOR reflect the stated proposition and research standard, not successful authenticated filing. CORROBORATED indicates supporting evidence with incomplete operational confirmation. UNRESOLVED and MANUAL VERIFICATION REQUIRED preserve missing information and review needs. Some later practitioner corrections retain a verified route label while their source/note explicitly identifies the practitioner basis; always read the source and note with the status.

Counts of jurisdictions, contact routes, answer sections, open questions and historical audit slots measure different things. Zero active contact research does not mean every plan’s case handling has been tested or all case-level questions are closed. Historical route-audit holds predate subsequent scoped corrections and are retained as historical records.

No live portal submission, external contact or new legal-research pass was performed for public packaging. External URLs can move, require authentication or become obsolete. Original captured evidence is not included; the source registry and retained hashes describe provenance without implying public access to those captures. Pattern checks are a screening aid, not a guarantee about every possible sensitive value.
