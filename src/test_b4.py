from test_b3 import db
from app import finalise_report,read_report,save_report,add_addendum
from pathlib import Path
import sqlite3

db.executescript(Path(__file__).with_name('locking.sql').read_text())
before=read_report(db,'t')['rooms']
r=finalise_report(db,'t');assert r['finalised_at'].endswith('Z')
assert finalise_report(db,'t')['finalised_at']==r['finalised_at']
try:save_report(db,{'tenancy':'t','rooms':before});raise AssertionError('Save not blocked')
except ValueError:pass
for sql in ["UPDATE room_entries SET note='changed'", "DELETE FROM photos", "UPDATE reports SET finalised_at=NULL"]:
 try:db.execute(sql);raise AssertionError(sql)
 except sqlite3.IntegrityError:pass
r=add_addendum(db,{'tenancy':'t','note':'Additional observation','created_at':'1900-01-01'})
assert r['rooms']==before
assert r['addenda'][0]['note']=='Additional observation'
assert r['addenda'][0]['created_at'].endswith('Z')
assert not r['addenda'][0]['created_at'].startswith('1900')
try:finalise_report(db,'other');raise AssertionError('Access')
except PermissionError:pass
print('PASS: finalise, stable system timestamp, locked saves/SQL edits, dated addendum, unchanged original and ownership')
