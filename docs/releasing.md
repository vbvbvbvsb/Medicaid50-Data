# Releasing

The repository is a public snapshot with a fresh history. Maintain the public JSON and provenance explicitly; never import the private working tree wholesale. Exclude client/case files, saved reviews, private captures, credentials and runtime databases. Check rights and source attribution for new contents.

Submit changes through a pull request from a topic branch. The required GitHub Actions `validate` check must pass, and the branch must be up to date with `main`, including for administrators. Regenerate `SHA256SUMS` even for documentation-only changes because it covers documentation too.

For a new release, update `metadata.public_release`, README counts/date, `NOTICE`, `CITATION.cff`, `datapackage.json`, provenance, changelog and release notes. Preserve field-level research dates rather than assigning the packaging date to all facts. The ZIP timestamp is fixed for deterministic builds and does not describe research currency.

```sh
git switch -c release/v1.0.1
python3 scripts/release.py --build
python3 scripts/release.py --check
git add .
git commit -m "Release reviewed dataset snapshot"
git push -u origin HEAD
gh pr create --base main --title "Release reviewed dataset snapshot" --body-file RELEASE_NOTES.md
gh pr checks --watch
gh pr merge --squash --delete-branch
git switch main
git pull --ff-only
git tag -a v1.0.1 -m "Medicaid50 Data v1.0.1"
git push origin v1.0.1
gh run list --workflow validate.yml --limit 5
```

Use the new version in commands for subsequent releases. The workflow in `.github/workflows/validate.yml` validates pushes and pull requests and supports manual runs. It runs the same checks and archive build shown above. Changes to workflow files require a credential authorized to manage GitHub Actions workflows. Pushing a stable version tag (`vMAJOR.MINOR.PATCH`) automatically starts validation and release publishing. No separate token or repository secret is needed; only the publishing job receives `contents: write` through GitHub’s built-in token. Compare release asset hashes after publication and verify the repository is public. Keep the dataset’s ODbL database license separate from MIT utility code and third-party source rights.

## Automatic publishing

Use the new version in all release metadata before creating its tag. The tag must exactly match `metadata.public_release.version`, `datapackage.json` and `CITATION.cff`, and its commit must already belong to `main` history. Prerelease tags and malformed versions are rejected. Existing `v1.0.0` remains the original release; do not move or re-push it.

On a version-tag push, the `validate` job tests the release gates, checks the tag and main ancestry, validates the committed JSON/CSVs/checksums, builds the archive and checks that building did not alter tracked files. It uploads the validated ZIP, asset `SHA256SUMS` and release notes as an intermediate workflow artifact.

The `publish` job depends on successful validation. It downloads that exact artifact, verifies the ZIP checksum again, creates a draft GitHub Release with the ZIP and checksum file attached, then makes it public. Validation failure skips publishing. Draft creation/upload failure leaves no new public release. An existing release is not overwritten; publishing that tag again fails. Inspect and remove an incomplete draft before retrying a failed publication.

Branch pushes, pull requests and manual workflow runs validate without publishing. Tag pushes made by a person using an authorized GitHub credential trigger publishing; tags created with another workflow’s built-in `GITHUB_TOKEN` do not trigger a new push workflow. GitHub Releases publication does not deploy the private application or change hosted database records.
