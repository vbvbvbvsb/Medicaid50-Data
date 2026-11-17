"""Exercise release gates without publishing anything. SPDX-License-Identifier: MIT"""
import json
import subprocess
import tempfile
import unittest
from pathlib import Path
from check_release import check_release

class ReleaseGateTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory(prefix='medicaid-release-gate-')
        self.addCleanup(self.temp.cleanup);self.root=Path(self.temp.name)
        self.run_git('init','-q','-b','main')
        self.run_git('config','user.email','ci@example.invalid');self.run_git('config','user.name','CI test')
        (self.root/'data').mkdir()
        (self.root/'data/medicaid_reporting_directory.json').write_text(json.dumps({'metadata':{'public_release':{'version':'1.2.3'}}}))
        (self.root/'datapackage.json').write_text(json.dumps({'version':'1.2.3'}))
        (self.root/'CITATION.cff').write_text('version: "1.2.3"\n')
        self.run_git('add','.');self.run_git('commit','-qm','Fixture')
        self.run_git('update-ref','refs/remotes/origin/main','HEAD');self.run_git('tag','v1.2.3')

    def run_git(self,*args):
        return subprocess.check_output(['git',*args],cwd=self.root,text=True,stderr=subprocess.PIPE).strip()

    def test_matching_tag_on_main_passes(self):
        self.assertEqual(check_release('v1.2.3',self.root),'1.2.3')

    def test_malformed_or_prerelease_tags_fail(self):
        for tag in ['v1.2.3-test','1.2.3','v01.2.3','v1.2','v1.2.3;echo bad']:
            with self.subTest(tag=tag),self.assertRaisesRegex(ValueError,'vMAJOR.MINOR.PATCH'):
                check_release(tag,self.root)

    def test_dataset_version_mismatch_fails(self):
        with self.assertRaisesRegex(ValueError,'public_release.version'):check_release('v1.2.4',self.root)

    def test_package_version_mismatch_fails(self):
        (self.root/'datapackage.json').write_text('{"version":"1.2.4"}')
        with self.assertRaisesRegex(ValueError,'datapackage'):check_release('v1.2.3',self.root)

    def test_citation_version_mismatch_fails(self):
        (self.root/'CITATION.cff').write_text('version: "1.2.4"\n')
        with self.assertRaisesRegex(ValueError,'CITATION'):check_release('v1.2.3',self.root)

    def test_different_checkout_fails(self):
        (self.root/'extra.txt').write_text('test');self.run_git('add','.');self.run_git('commit','-qm','New commit')
        with self.assertRaisesRegex(ValueError,'Checkout'):check_release('v1.2.3',self.root)

    def test_tag_outside_main_fails(self):
        self.run_git('switch','-qc','unreviewed')
        (self.root/'extra.txt').write_text('test');self.run_git('add','.');self.run_git('commit','-qm','Unreviewed commit')
        self.run_git('tag','-f','v1.2.3')
        with self.assertRaisesRegex(ValueError,'main history'):check_release('v1.2.3',self.root)

if __name__=='__main__':unittest.main()
