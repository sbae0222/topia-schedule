#!/usr/bin/env python3
"""Build the public faculty page from a sanitized, approved schedule snapshot."""
import argparse, hashlib, json, re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
HERE=Path(__file__).resolve().parent
def main():
 p=argparse.ArgumentParser()
 p.add_argument('--data',type=Path,default=HERE/'schedule-december-2026.json')
 p.add_argument('--template',type=Path,default=HERE/'faculty_template.html')
 p.add_argument('--output',type=Path,default=ROOT/'index.html')
 args=p.parse_args()
 d=json.loads(args.data.read_text(encoding='utf-8'))
 assert set(d)=={'version','term','updatedKst','teachers','groups','classes','closing','available','rosterUrl','availabilityNotes'}
 assert d['term']=='2026-12'
 names={x['key'] for x in d['teachers']}
 assert len(names)==len(d['teachers'])
 assert len({r['code'] for r in d['classes']})==len(d['classes'])
 for r in d['classes']:
  assert set(r)=={'code','level','group','teacher','isNew','duplicate','currentCount','scheduledCount','registeredCount','pendingCount'}
  assert re.fullmatch(r'(?:GW|GD|SG|SR)[1-5]',r['level'])
  assert re.fullmatch(r'(?:GW|GD|SG|SR)[1-5]_\d+\([^)]+\)',r['code'])
  assert all(isinstance(r[k],int) and r[k]>=0 for k in ['currentCount','scheduledCount','registeredCount','pendingCount'])
  assert r['registeredCount']==r['currentCount']+r['scheduledCount']
  assert r['teacher'] in names and r['group'] in d['groups']
 for g,ts in d['available'].items():
  assert g in d['groups'] and set(ts)<=names
  assert not any(r['group']==g and r['teacher'] in ts for r in d['classes'])
 template=args.template.read_text(encoding='utf-8')
 assert template.startswith('<!DOCTYPE html>') and template.count('__SCHEDULE_DATA__')==1
 payload=json.dumps(d,ensure_ascii=False,separators=(',',':')).replace('</',r'<\/')
 html=template.replace('__SCHEDULE_DATA__',payload)
 assert not re.search(r'\b01[016789]-\d{3,4}-\d{4}\b|examineeId|examNumber|privateRosters|publicRosters|counseling|paidAt|SUPABASE|SERVICE_ROLE|api[_-]?key',html,re.I)
 args.output.parent.mkdir(parents=True,exist_ok=True)
 args.output.write_text(html,encoding='utf-8',newline='\n')
 print(json.dumps({'output':str(args.output),'classes':len(d['classes']),'new':sum(r['isNew'] for r in d['classes']),'teachers':len(d['teachers']),'sha256':hashlib.sha256(html.encode()).hexdigest()},ensure_ascii=False))
if __name__=='__main__':main()

