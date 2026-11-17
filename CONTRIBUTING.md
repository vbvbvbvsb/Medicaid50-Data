# Contributing corrections

Open an issue or pull request with the jurisdiction, record or fact path, the current value, proposed correction, official public source URL, access date, relevant page/section, claim type, program and transaction scope. Explain whether it changes a new-case destination, an existing-case action, a plan contact or a legal notice requirement.

Prefer agency, contractor and plan sources. Label practitioner observations explicitly and distinguish them from independently available published evidence. Preserve historical/service-date qualifications. Do not infer a statewide attorney route from a provider portal, general contact number, plan award or existing-case service.

Do not post client names, member IDs, SSNs, birth dates, case numbers, demand letters, nonpublic correspondence or credentials. Supply a non-identifying summary when reporting practitioner experience.

Database contributions must be available for incorporation under ODbL 1.0; utility code contributions under MIT. Identify any separately protected third-party content and its terms. Do not submit copied source documents without permission. Contributions do not assert rights you do not hold.

After editing the JSON, run `python3 scripts/release.py --build`, then `python3 scripts/release.py --check`. Include regenerated CSVs, validation output and checksums. Maintainers review source support and scope before accepting a change; passing structural checks is not factual verification.
