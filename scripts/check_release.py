"""Check stable version tags against release metadata and reviewed main history.

SPDX-License-Identifier: MIT
"""
import argparse
import json
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def git(root, *args):
    return subprocess.check_output(['git', *args], cwd=root, text=True, stderr=subprocess.PIPE).strip()

def check_release(tag, root=ROOT):
    if not re.fullmatch(r'v(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)', tag):
        raise ValueError('Release tag must use vMAJOR.MINOR.PATCH (stable versions only).')
    version = tag[1:]
    directory = json.loads((root/'data/medicaid_reporting_directory.json').read_text())
    package = json.loads((root/'datapackage.json').read_text())
    citation = (root/'CITATION.cff').read_text()
    if directory['metadata']['public_release']['version'] != version:
        raise ValueError('Tag does not match metadata.public_release.version.')
    if package['version'] != version:
        raise ValueError('Tag does not match datapackage.json version.')
    if not re.search(r'^version: "'+re.escape(version)+r'"$', citation, re.MULTILINE):
        raise ValueError('Tag does not match CITATION.cff version.')
    if git(root, 'rev-parse', tag+'^{commit}') != git(root, 'rev-parse', 'HEAD'):
        raise ValueError('Checkout must match the version tag exactly.')
    result = subprocess.run(['git','merge-base','--is-ancestor','HEAD','refs/remotes/origin/main'],cwd=root,check=False)
    if result.returncode != 0:
        raise ValueError('Release commit must already be in origin/main history.')
    return version

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--tag',required=True);args=parser.parse_args()
    try: version=check_release(args.tag)
    except (ValueError,KeyError,subprocess.CalledProcessError) as error:
        raise SystemExit('Release gate failed: '+str(error))
    print('PASS: release tag, metadata and main history match version '+version)

if __name__=='__main__':main()
