"""Generate exports, validate the database and build deterministic release assets.

SPDX-License-Identifier: MIT
"""
import argparse
import csv
import hashlib
import io
import json
import re
import zipfile
from pathlib import Path
from schema_check import validate_schema

ROOT = Path(__file__).resolve().parents[1]
SECTIONS = ['identification','administration','personal_injury','workers_compensation','workflow']
SUPPORTED = {'VERIFIED — PRIMARY', 'VERIFIED — CONTRACTOR'}
EXPECTED_CODES = set('AL AK AZ AR CA CO CT DE DC FL GA HI ID IL IN IA KS KY LA ME MD MA MI MN MS MO MT NE NV NH NJ NM NY NC ND OH OK OR PA RI SC SD TN TX UT VT VA WA WV WI WY'.split())

def read(path): return json.loads((ROOT / path).read_text())
def dump(value): return json.dumps(value,ensure_ascii=False,indent=2)+'\n'
def facts(s):
    for section in SECTIONS:
        for key,value in s[section].items(): yield section+'.'+key,value
    yield 'clarification_contact',s['clarification_contact']

def csv_text(rows):
    keys = list(dict.fromkeys(k for row in rows for k in row))
    def cell(v):
        if v is None: return ''
        value = json.dumps(v,ensure_ascii=False,sort_keys=True) if isinstance(v,(list,dict)) else str(v)
        # Excel-safe exports. The JSON preserves the original value exactly.
        return "'"+value if re.match(r'^[\s]*[=+@-]',value) else value
    out=io.StringIO(newline=''); writer=csv.writer(out,lineterminator='\r\n')
    writer.writerow(keys)
    writer.writerows([[cell(row.get(k)) for k in keys] for row in rows])
    return out.getvalue()

def exports(d):
    result = {}
    for section in ['states','managed_care_routes','portal_directory','candidate_portals','verification_queue','sources','vendor_matrix']:
        result['data/csv/'+section+'.csv'] = csv_text(d[section])
    result['data/csv/field_level_evidence.csv'] = csv_text([
      {'state':s['state_code'],'field':p,**f} for s in d['states'] for p,f in facts(s)])
    workflows=d['practitioner_workflows']
    result['data/csv/practitioner_questions.csv']=csv_text(workflows['questions'])
    result['data/csv/practitioner_answers.csv']=csv_text([
      {'state':code,**a} for code,state in workflows['states'].items() for a in state['answers']])
    return result

def walk(value,path='$'):
    if isinstance(value,dict):
        for k,v in value.items(): yield from walk(v,path+'.'+k)
    elif isinstance(value,list):
        for i,v in enumerate(value): yield from walk(v,f'{path}[{i}]')
    else: yield path,value

def validate(d):
    validate_schema(d,read('data/medicaid_directory.schema.json'))
    codes=[s['state_code'] for s in d['states']]
    assert len(codes)==51 and set(codes)==EXPECTED_CODES,'Jurisdiction coverage'
    ids=[s['source_id'] for s in d['sources']]
    assert len(ids)==len(set(ids)),'Duplicate source IDs'
    ids=set(ids)
    def refs(x,path='$'):
        if isinstance(x,dict):
            for k,v in x.items():
                if k in {'source_ids','canonical_source_ids'}:
                    assert isinstance(v,list) and set(v)<=ids,(path,k,'unknown source IDs',set(v)-ids)
                elif k=='source_id': assert v in ids,(path,k,v)
                refs(v,path+'.'+k)
        elif isinstance(x,list):
            for i,v in enumerate(x):refs(v,f'{path}[{i}]')
    refs(d)
    for s in d['sources']: assert re.match(r'^https?://',s['url']),(s['source_id'],'source URL')
    for s in d['states']:
        for path,f in facts(s):
            if f['status'] in SUPPORTED: assert f['value'] and f['source_ids'] and f['verified_on'],(s['state_code'],path)
        for prefix,section in [('pi','personal_injury'),('wc','workers_compensation')]:
            assert s['verification'][prefix+'_initial_status']==s[section]['initial_reporting_method']['status']
    assert len({(r['state'],r['plan']) for r in d['managed_care_routes']})==len(d['managed_care_routes'])
    assert len({r['portal_id'] for r in d['portal_directory']})==len(d['portal_directory'])
    for p,v in walk(d):
        if isinstance(v,str):
            assert not re.search(r'workspace-439221|/Users/|file://|localhost|127\.0\.0\.1|gh[opusr]_[A-Za-z0-9]{20,}|\b\d{3}-\d{2}-\d{4}\b',v),(p,'private reference or sensitive-value pattern')
    c=d['metadata']['coverage']
    for key,actual in [('states',len(codes)),('sources',len(ids)),('plan_routes',len(d['managed_care_routes'])),('portals',len(d['portal_directory']))]: assert c[key]==actual,(key,'stale count')
    for prefix,sec in [('pi','personal_injury'),('wc','workers_compensation')]:
        assert c[prefix+'_initial_verified']==sum(s[sec]['initial_reporting_method']['status'] in SUPPORTED for s in d['states'])
    return {'jurisdictions':len(codes),'managed_care_routes':len(d['managed_care_routes']),'sources':len(ids),'portals':len(d['portal_directory']),'practitioner_questions':len(d['practitioner_workflows']['questions']),'practitioner_answers':sum(len(s['answers']) for s in d['practitioner_workflows']['states'].values()),'schema':'PASS','source_references':'PASS','sensitive_pattern_scan':'PASS','external_links_reverified':False}

def payload_files():
    return sorted(p for p in ROOT.rglob('*') if p.is_file() and not any(part in {'.git','dist','__pycache__'} for part in p.relative_to(ROOT).parts) and p.name != 'SHA256SUMS')

def checksums():
    return ''.join(hashlib.sha256(p.read_bytes()).hexdigest()+'  '+p.relative_to(ROOT).as_posix()+'\n' for p in payload_files())

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--check',action='store_true');parser.add_argument('--build',action='store_true');args=parser.parse_args()
    assert not (args.check and args.build)
    d=read('data/medicaid_reporting_directory.json'); report=validate(d)
    for name,text in {**exports(d),'validation.json':dump(report)}.items():
        p=ROOT/name
        if args.check: assert p.read_bytes()==text.encode(),('Stale generated file',name)
        else: p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(text.encode())
    sums=checksums()
    if args.check: assert (ROOT/'SHA256SUMS').read_text()==sums,'Checksum mismatch'
    else: (ROOT/'SHA256SUMS').write_text(sums)
    if args.build:
        version=d['metadata']['public_release']['version']; dist=ROOT/'dist';dist.mkdir(exist_ok=True)
        asset=dist/f'Medicaid50-Data-v{version}.zip'
        with zipfile.ZipFile(asset,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
            for p in sorted(payload_files()+[ROOT/'SHA256SUMS']):
                info=zipfile.ZipInfo(f'Medicaid50-Data-v{version}/'+p.relative_to(ROOT).as_posix(),date_time=(2026,11,16,0,0,0));info.compress_type=zipfile.ZIP_DEFLATED;info.external_attr=0o100644<<16
                z.writestr(info,p.read_bytes())
        (dist/'SHA256SUMS').write_text(hashlib.sha256(asset.read_bytes()).hexdigest()+'  '+asset.name+'\n')
        print('Built',asset.name)
    print(dump(report))

if __name__=='__main__':main()
