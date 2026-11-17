# Releasing

The repository is a public snapshot with a fresh history. Maintain the public JSON and provenance explicitly; never import the private working tree wholesale. Exclude client/case files, saved reviews, private captures, credentials and runtime databases. Check rights and source attribution for new contents.

For a new release, update `metadata.public_release`, README counts/date, `NOTICE`, `CITATION.cff`, `datapackage.json`, provenance, changelog and release notes. Preserve field-level research dates rather than assigning the packaging date to all facts. The ZIP timestamp is fixed for deterministic builds and does not describe research currency.

```sh
python3 scripts/release.py --build
python3 scripts/release.py --check
git add .
git commit -m "Release reviewed dataset snapshot"
git tag -a v1.0.0 -m "Medicaid50 Data v1.0.0"
git push origin main --follow-tags
gh release create v1.0.0 dist/Medicaid50-Data-v1.0.0.zip dist/SHA256SUMS --title "Medicaid50 Data v1.0.0" --notes-file RELEASE_NOTES.md
```

Use the new version in commands for subsequent releases. The workflow in `.github/workflows/validate.yml` validates pushes and pull requests and supports manual runs. It runs the same checks and archive build shown above. Changes to workflow files require a credential authorized to manage GitHub Actions workflows. Publication is performed explicitly through GitHub Releases. Compare release asset hashes after upload and verify the repository is public. Keep the dataset’s ODbL database license separate from MIT utility code and third-party source rights.
