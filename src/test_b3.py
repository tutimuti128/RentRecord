import sqlite3
from pathlib import Path
from app import read_report, save_report

db=sqlite3.connect(':memory:');db.row_factory=sqlite3.Row
db.executescript(Path(__file__).with_name('schema.sql').read_text())
db.execute("INSERT INTO users VALUES ('demo','Demo','demo@example.test','tenant')")
db.execute("INSERT INTO tenancies(id,owner_id,address,landlord_name,landlord_email,rent_cents,deposit_cents,start_date) VALUES ('t','demo','Example','Demo','demo@example.test',80000,160000,'2026-11-10')")
r=read_report(db,'t');assert len(r['rooms'])==6
rooms=r['rooms'];rooms[0]['note']='Scratch on wall';rooms[0]['condition']='minor issue'
rooms[0]['photos']=['data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8/x8AAwMCAO+aD1sAAAAASUVORK5CYII=']
save_report(db,{'tenancy':'t','rooms':rooms})
r=read_report(db,'t');assert r['rooms'][0]['note']=='Scratch on wall';assert len(r['rooms'][0]['photos'])==1
save_report(db,{'tenancy':'t','rooms':r['rooms'][:-1]});assert len(read_report(db,'t')['rooms'])==5
try:read_report(db,'other');raise AssertionError('access')
except PermissionError:pass
bad=read_report(db,'t')['rooms'];bad[0]['photos']=['data:text/html;base64,PGgxPg==']
try:save_report(db,{'tenancy':'t','rooms':bad});raise AssertionError('image validation')
except ValueError:pass
assert len(read_report(db,'t')['rooms'][0]['photos'])==1
print('PASS: default rooms, saved notes/conditions/photos, room removal, access denial and invalid image rejection')
