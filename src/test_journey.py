from test_b4 import db
from app import journey,update_journey
import json

db.execute('CREATE TABLE journeys(tenancy_id TEXT PRIMARY KEY REFERENCES tenancies(id),payload TEXT NOT NULL)')
j=journey(db,'t');assert len(j['checklist'])==6
j['checklist']=[True]*6;j['meters']='123';j['reminder']=7
assert update_journey(db,{'tenancy':'t','value':j})['meters']=='123'
try:update_journey(db,{'tenancy':'t','action':'stage','stage':'Returned in full'});raise AssertionError('transition')
except ValueError:pass
for stage in ['Keys returned','Deposit requested','Returned in part','Returned in full']:
 result=update_journey(db,{'tenancy':'t','action':'stage','stage':stage})
assert len(result['events'])==4
assert all(e['date'].endswith('Z') for e in result['events'])
j=journey(db,'t');j['events']=[]
assert len(update_journey(db,{'tenancy':'t','value':j})['events'])==4
try:journey(db,'other');raise AssertionError('owner')
except PermissionError:pass
print('PASS: checklist persistence, stage transitions, server dates, history preservation and owner checks')
