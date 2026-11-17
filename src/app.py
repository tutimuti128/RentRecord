"""Local B2 demo: one fictional tenant, SQLite persistence, no external dependencies."""
import json, sqlite3, secrets, webbrowser, base64
from urllib.parse import urlparse, parse_qs
from pathlib import Path
from decimal import Decimal, InvalidOperation
from datetime import date
from http.server import BaseHTTPRequestHandler, HTTPServer

ROOT = Path(__file__).parent
TOKEN = secrets.token_urlsafe(32)
ACTOR = 'demo'

def connect():
    db = sqlite3.connect(ROOT / 'rentrecord.sqlite3')
    db.row_factory = sqlite3.Row
    db.execute('PRAGMA foreign_keys=ON')
    return db

def validate(data):
    result = {}
    for key in ('address','landlord_name','landlord_email','start_date'):
        value = data.get(key)
        if not isinstance(value,str) or not value.strip() or len(value)>300:
            raise ValueError('Please complete all fields (maximum 300 characters each).')
        result[key] = value.strip()
    if '@' not in result['landlord_email'] or '.' not in result['landlord_email'].split('@')[-1]:
        raise ValueError('Enter a valid landlord email.')
    date.fromisoformat(result['start_date'])
    for key in ('rent','deposit'):
        try:
            number = Decimal(str(data.get(key,'')))
            if not number.is_finite() or number<0 or number>10000000 or (key=='rent' and number==0) or number*100 != (number*100).to_integral_value():
                raise ValueError('Enter valid amounts with at most two decimal places; rent must be positive.')
            result[key+'_cents'] = int(number*100)
        except InvalidOperation:
            raise ValueError('Enter valid amounts.')
    return result

DEFAULT_ROOMS = ['Entrance','Kitchen','Bathroom','Living room','Bedroom','Balcony / storage']

def report(db, tenancy):
    if not db.execute('SELECT id FROM tenancies WHERE id=? AND owner_id=?',(tenancy,ACTOR)).fetchone():
        raise PermissionError('Tenancy unavailable')
    row=db.execute("SELECT * FROM reports WHERE tenancy_id=? AND type='move-in'",(tenancy,)).fetchone()
    if not row:
        rid=secrets.token_urlsafe(16)
        db.execute("INSERT INTO reports(id,tenancy_id,type) VALUES (?,?,'move-in')",(rid,tenancy))
        for name in DEFAULT_ROOMS:
            db.execute("INSERT INTO room_entries(id,report_id,room_name,condition) VALUES (?,?,?,'OK')",(secrets.token_urlsafe(16),rid,name))
        row=db.execute('SELECT * FROM reports WHERE id=?',(rid,)).fetchone()
    return row

def read_report(db, tenancy):
    row=report(db,tenancy)
    rooms=[]
    for entry in db.execute('SELECT * FROM room_entries WHERE report_id=? ORDER BY rowid',(row['id'],)):
        item=dict(entry)
        item['photos']=[r[0] for r in db.execute('SELECT storage_key FROM photos WHERE room_entry_id=? ORDER BY rowid',(entry['id'],))]
        rooms.append(item)
    return {'rooms':rooms,'finalised_at':row['finalised_at'],'addenda':[dict(a) for a in db.execute('SELECT note,created_at FROM addenda WHERE report_id=? ORDER BY rowid',(row['id'],))]}

def save_report(db,data):
    row=report(db,data.get('tenancy'))
    if row['finalised_at']: raise ValueError('This report is locked.')
    rooms=data.get('rooms')
    if not isinstance(rooms,list) or not 1<=len(rooms)<=30: raise ValueError('Include between 1 and 30 rooms.')
    total=0
    for r in rooms:
        if not isinstance(r,dict) or not isinstance(r.get('room_name'),str) or not 1<=len(r['room_name'].strip())<=100: raise ValueError('Enter a room name (up to 100 characters).')
        if r.get('condition') not in ('OK','minor issue','defect'): raise ValueError('Choose a valid condition.')
        if not isinstance(r.get('note'),str) or len(r['note'])>5000: raise ValueError('Notes must be under 5,000 characters.')
        if not isinstance(r.get('photos'),list) or len(r['photos'])>10: raise ValueError('Maximum 10 photos per room.')
        for photo in r['photos']:
            if not isinstance(photo,str) or ',' not in photo: raise ValueError('Invalid photo.')
            head,encoded=photo.split(',',1)
            raw=base64.b64decode(encoded,validate=True)
            valid=(head=='data:image/jpeg;base64' and raw.startswith(b'\xff\xd8\xff')) or (head=='data:image/png;base64' and raw.startswith(b'\x89PNG\r\n\x1a\n')) or (head=='data:image/webp;base64' and raw.startswith(b'RIFF') and raw[8:12]==b'WEBP')
            if not valid or len(raw)>3*1024*1024: raise ValueError('Use JPEG, PNG or WebP photos under 3 MB each.')
            total+=len(raw)
    if total>20*1024*1024: raise ValueError('Report photos must total under 20 MB.')
    db.execute('DELETE FROM room_entries WHERE report_id=?',(row['id'],))
    for r in rooms:
        rid=secrets.token_urlsafe(16)
        db.execute('INSERT INTO room_entries(id,report_id,room_name,condition,note) VALUES (?,?,?,?,?)',(rid,row['id'],r['room_name'].strip(),r['condition'],r['note']))
        for photo in r['photos']:
            db.execute('INSERT INTO photos(id,room_entry_id,storage_key) VALUES (?,?,?)',(secrets.token_urlsafe(16),rid,photo))

def finalise_report(db, tenancy):
    row=report(db,tenancy)
    if not row['finalised_at']:
        db.execute("UPDATE reports SET finalised_at=strftime('%Y-%m-%dT%H:%M:%fZ','now') WHERE id=? AND finalised_at IS NULL",(row['id'],))
    return read_report(db,tenancy)

def add_addendum(db,data):
    row=report(db,data.get('tenancy'))
    if not row['finalised_at']: raise ValueError('Finalise the report before adding an addendum.')
    note=data.get('note')
    if not isinstance(note,str) or not 1<=len(note.strip())<=5000:
        raise ValueError('Enter an addendum of 1–5,000 characters.')
    db.execute("INSERT INTO addenda(id,report_id,note,created_at) VALUES (?,?,?,strftime('%Y-%m-%dT%H:%M:%fZ','now'))",(secrets.token_urlsafe(16),row['id'],note.strip()))
    return read_report(db,data['tenancy'])

BILL_CATEGORIES=['Rent','Electricity','Water','Internet','Insurance','Other']
OFFERS=[
    {'id':'sample-cafe','business':'Harbor Café (sample)','category':'Restaurant','location':'Helsinki','benefit':'10% off one coffee and pastry','terms':'Example offer for the prototype. Not redeemable.','expires':'2027-12-31'},
    {'id':'sample-market','business':'Market Corner (sample)','category':'Groceries','location':'Espoo','benefit':'€3 off a €25 basket','terms':'Example offer for the prototype. Not redeemable.','expires':'2027-12-31'},
    {'id':'sample-laundry','business':'FreshFold Laundry (sample)','category':'Home services','location':'Helsinki','benefit':'First wash 15% off','terms':'Example offer for the prototype. Not redeemable.','expires':'2027-12-31'},
]

def validate_bill(data):
    tenancy=data.get('tenancy')
    if not isinstance(tenancy,str) or not tenancy: raise ValueError('Choose a tenancy.')
    if not isinstance(data.get('provider'),str) or not 1<=len(data['provider'].strip())<=120: raise ValueError('Enter a provider name.')
    category=data.get('category')
    if category not in BILL_CATEGORIES: raise ValueError('Choose a valid bill category.')
    try:
        amount=Decimal(str(data.get('amount','')))
        if not amount.is_finite() or amount<=0 or amount>10000000 or amount*100 != (amount*100).to_integral_value(): raise ValueError('Enter a positive amount with up to two decimals.')
        due=date.fromisoformat(data.get('due_date',''))
    except (InvalidOperation,TypeError): raise ValueError('Enter a valid amount and due date.')
    note=data.get('note','')
    if not isinstance(note,str) or len(note)>500: raise ValueError('Note must be under 500 characters.')
    return tenancy,data['provider'].strip(),category,int(amount*100),due.isoformat(),note.strip()

def get_bills(db,tenancy):
    if not db.execute('SELECT id FROM tenancies WHERE id=? AND owner_id=?',(tenancy,ACTOR)).fetchone(): raise PermissionError('Tenancy unavailable')
    return [dict(r) for r in db.execute('SELECT id,provider,category,amount_cents,due_date,paid,note,created_at FROM bills WHERE tenancy_id=? ORDER BY due_date,created_at',(tenancy,))]

def create_bill(db,data):
    tenancy,provider,category,amount,due,note=validate_bill(data)
    if not db.execute('SELECT id FROM tenancies WHERE id=? AND owner_id=?',(tenancy,ACTOR)).fetchone(): raise PermissionError('Tenancy unavailable')
    bill_id=secrets.token_urlsafe(16)
    db.execute('INSERT INTO bills(id,tenancy_id,provider,category,amount_cents,due_date,note) VALUES(?,?,?,?,?,?,?)',(bill_id,tenancy,provider,category,amount,due,note))
    return get_bills(db,tenancy)

def update_bill(db,data):
    tenancy=data.get('tenancy');bill_id=data.get('bill_id');action=data.get('action')
    if not isinstance(tenancy,str) or not isinstance(bill_id,str): raise ValueError('Invalid bill.')
    if not db.execute('SELECT id FROM tenancies WHERE id=? AND owner_id=?',(tenancy,ACTOR)).fetchone(): raise PermissionError('Tenancy unavailable')
    row=db.execute('SELECT id FROM bills WHERE id=? AND tenancy_id=?',(bill_id,tenancy)).fetchone()
    if not row: raise PermissionError('Bill unavailable')
    if action=='edit':
        _,provider,category,amount,due,note=validate_bill(data)
        if data.get('tenancy')!=tenancy: raise ValueError('Tenancy mismatch.')
        db.execute('UPDATE bills SET provider=?,category=?,amount_cents=?,due_date=?,note=? WHERE id=? AND tenancy_id=?',(provider,category,amount,due,note,bill_id,tenancy))
    elif action=='paid': db.execute('UPDATE bills SET paid=1 WHERE id=? AND tenancy_id=?',(bill_id,tenancy))
    elif action=='unpaid': db.execute('UPDATE bills SET paid=0 WHERE id=? AND tenancy_id=?',(bill_id,tenancy))
    elif action=='delete': db.execute('DELETE FROM bills WHERE id=? AND tenancy_id=?',(bill_id,tenancy))
    else: raise ValueError('Invalid bill action.')
    return get_bills(db,tenancy)

CHECKLIST=['Cleaning done','Meter readings noted','All keys returned','Forwarding address given','Final inspection date booked','Move-out photos taken']
STAGES=['Not yet moved out','Keys returned','Deposit requested','Returned in full','Returned in part','Disputed']

def journey(db,tenancy):
    report(db,tenancy) # owner check
    row=db.execute('SELECT payload FROM journeys WHERE tenancy_id=?',(tenancy,)).fetchone()
    return json.loads(row[0]) if row else {'checklist':[False]*6,'photos':{},'events':[],'reminder':14,'inspection_date':'','meters':'','forwarding':''}

def update_journey(db,data):
    tenancy=data.get('tenancy');old=journey(db,tenancy)
    if data.get('action')=='stage':
        stage=data.get('stage')
        if stage not in STAGES[1:]: raise ValueError('Choose a valid stage.')
        current=old['events'][-1]['stage'] if old['events'] else STAGES[0]
        allowed={STAGES[0]:['Keys returned'],'Keys returned':['Deposit requested'],'Deposit requested':['Returned in full','Returned in part','Disputed'],'Returned in part':['Returned in full','Disputed'],'Disputed':['Returned in full','Returned in part'],'Returned in full':[]}
        if stage not in allowed[current]: raise ValueError('Complete the previous deposit step first.')
        old['events'].append({'stage':stage,'date':db.execute("SELECT strftime('%Y-%m-%dT%H:%M:%fZ','now')").fetchone()[0]})
    else:
        value=data.get('value')
        if not isinstance(value,dict): raise ValueError('Invalid checklist.')
        checks=value.get('checklist')
        if not isinstance(checks,list) or len(checks)!=6 or any(type(v)!=bool for v in checks): raise ValueError('Invalid checklist.')
        reminder=value.get('reminder')
        if type(reminder)!=int or not 1<=reminder<=365: raise ValueError('Reminder must be 1–365 days.')
        photos=value.get('photos',{})
        if not isinstance(photos,dict) or len(photos)>30: raise ValueError('Invalid photos.')
        total=0
        for name,items in photos.items():
            if not isinstance(name,str) or len(name)>150 or not isinstance(items,list) or len(items)>10: raise ValueError('Invalid room photos.')
            for photo in items:
                if not isinstance(photo,str) or ',' not in photo: raise ValueError('Invalid photo.')
                head,encoded=photo.split(',',1);raw=base64.b64decode(encoded,validate=True)
                valid=(head=='data:image/jpeg;base64' and raw.startswith(b'\xff\xd8\xff')) or (head=='data:image/png;base64' and raw.startswith(b'\x89PNG\r\n\x1a\n')) or (head=='data:image/webp;base64' and raw.startswith(b'RIFF') and raw[8:12]==b'WEBP')
                if not valid or len(raw)>3*1024*1024: raise ValueError('Use JPEG, PNG or WebP under 3 MB.')
                total+=len(raw)
        if total>20*1024*1024: raise ValueError('Move-out photos exceed 20 MB.')
        for key in ['inspection_date','meters','forwarding']:
            v=value.get(key,'')
            if not isinstance(v,str) or len(v)>1000: raise ValueError('Invalid detail.')
            old[key]=v
        old.update(checklist=checks,reminder=reminder,photos=photos)
    db.execute('INSERT INTO journeys(tenancy_id,payload) VALUES (?,?) ON CONFLICT(tenancy_id) DO UPDATE SET payload=excluded.payload',(tenancy,json.dumps(old)))
    return old

class Handler(BaseHTTPRequestHandler):
    def reply(self,status,body,kind='application/json'):
        content = body.encode() if isinstance(body,str) else json.dumps(body).encode()
        self.send_response(status)
        self.send_header('Content-Type',kind+'; charset=utf-8')
        self.send_header('Cache-Control','no-store')
        self.send_header('X-Content-Type-Options','nosniff')
        self.end_headers()
        self.wfile.write(content)
    def allowed(self):
        return self.headers.get('Host') == '127.0.0.1:8000'
    def do_GET(self):
        if not self.allowed(): return self.reply(403,{'error':'Access denied'})
        if self.path=='/':
            return self.reply(200,(ROOT/'index.html').read_text().replace('__TOKEN__',TOKEN),'text/html')
        if self.path=='/api/offers': return self.reply(200,OFFERS)
        if urlparse(self.path).path=='/api/bills':
            try:
                tenancy=parse_qs(urlparse(self.path).query).get('tenancy',[''])[0]
                with connect() as db: result=get_bills(db,tenancy)
                return self.reply(200,result)
            except PermissionError: return self.reply(403,{'error':'Tenancy unavailable'})
        if urlparse(self.path).path=='/api/journey':
            try:
                with connect() as db: result=journey(db,parse_qs(urlparse(self.path).query).get('tenancy',[''])[0])
                return self.reply(200,result)
            except PermissionError: return self.reply(403,{'error':'Tenancy unavailable'})
        if urlparse(self.path).path=='/api/report':
            try:
                with connect() as db:
                    result=read_report(db,parse_qs(urlparse(self.path).query).get('tenancy',[''])[0])
                return self.reply(200,result)
            except PermissionError: return self.reply(403,{'error':'Tenancy unavailable'})
        if self.path=='/api/tenancies':
            with connect() as db:
                rows = db.execute('SELECT * FROM tenancies WHERE owner_id=? ORDER BY created_at DESC,rowid DESC',(ACTOR,)).fetchall()
            return self.reply(200,[dict(row) for row in rows])
        self.reply(404,{'error':'Not found'})
    def do_POST(self):
        if not self.allowed() or self.headers.get('X-Demo-Token')!=TOKEN:
            return self.reply(403,{'error':'Access denied; reload the page.'})
        if self.path=='/api/bills':
            try:
                length=int(self.headers.get('Content-Length','0'))
                if not 0<length<10000: raise ValueError('Invalid request size.')
                data=json.loads(self.rfile.read(length))
                with connect() as db:
                    db.execute('BEGIN IMMEDIATE')
                    result=create_bill(db,data) if data.get('action','create')=='create' else update_bill(db,data)
                return self.reply(200,result)
            except PermissionError: return self.reply(403,{'error':'Bill or tenancy unavailable'})
            except (ValueError,TypeError,AttributeError) as e: return self.reply(400,{'error':str(e)})
            except sqlite3.Error: return self.reply(500,{'error':'Could not save bill.'})
        if self.path=='/api/journey':
            try:
                length=int(self.headers.get('Content-Length','0'))
                if not 0<length<29*1024*1024: raise ValueError('Upload too large.')
                data=json.loads(self.rfile.read(length))
                with connect() as db: result=update_journey(db,data)
                return self.reply(200,result)
            except PermissionError: return self.reply(403,{'error':'Tenancy unavailable'})
            except (ValueError,TypeError,AttributeError) as e: return self.reply(400,{'error':str(e)})
            except sqlite3.Error: return self.reply(500,{'error':'Could not save.'})
        if self.path in ('/api/finalise','/api/addendum'):
            try:
                length=int(self.headers.get('Content-Length','0'))
                if not 0<length<30000: raise ValueError('Request too large.')
                data=json.loads(self.rfile.read(length))
                with connect() as db:
                    db.execute('BEGIN IMMEDIATE')
                    result=finalise_report(db,data.get('tenancy')) if self.path=='/api/finalise' else add_addendum(db,data)
                return self.reply(200,result)
            except PermissionError: return self.reply(403,{'error':'Tenancy unavailable'})
            except (ValueError,TypeError,AttributeError) as e: return self.reply(400,{'error':str(e)})
            except sqlite3.Error: return self.reply(409,{'error':'The report could not be changed. Reload and try again.'})
        if self.path=='/api/report':
            try:
                length=int(self.headers.get('Content-Length','0'))
                if not 0<length<29*1024*1024: raise ValueError('Report too large (20 MB total photos).')
                data=json.loads(self.rfile.read(length))
                with connect() as db: save_report(db,data)
                return self.reply(200,{'saved':True})
            except PermissionError: return self.reply(403,{'error':'Tenancy unavailable'})
            except (ValueError,TypeError,AttributeError) as e: return self.reply(400,{'error':str(e)})
            except sqlite3.Error: return self.reply(500,{'error':'Could not save report.'})
        if self.path!='/api/tenancies': return self.reply(404,{'error':'Not found'})
        try:
            length=int(self.headers.get('Content-Length','0'))
            if not 0<length<10000: raise ValueError('Invalid request size.')
            data=json.loads(self.rfile.read(length))
            values=validate(data)
            if values['deposit_cents']>3*values['rent_cents'] and data.get('acknowledged') is not True:
                return self.reply(422,{'error':'Deposit exceeds three months of rent. Please acknowledge the warning.'})
            with connect() as db:
                db.execute('INSERT INTO tenancies(id,owner_id,address,landlord_name,landlord_email,rent_cents,deposit_cents,start_date) VALUES (?,?,?,?,?,?,?,?)',(secrets.token_urlsafe(16),ACTOR,values['address'],values['landlord_name'],values['landlord_email'],values['rent_cents'],values['deposit_cents'],values['start_date']))
            self.reply(201,{'saved':True})
        except (ValueError,TypeError,AttributeError):
            self.reply(400,{'error':'Check your fields: valid date, email, positive rent and non-negative deposit with at most two decimal places.'})
        except sqlite3.Error:
            self.reply(500,{'error':'Could not save. Please try again.'})

if __name__=='__main__':
    with connect() as db:
        if not db.execute("SELECT name FROM sqlite_master WHERE name='users'").fetchone():
            db.executescript((ROOT/'schema.sql').read_text())
        db.execute("INSERT OR IGNORE INTO users VALUES ('demo','Demo Tenant','tenant@example.test','tenant')")
        db.executescript((ROOT/'locking.sql').read_text())
        db.execute('CREATE TABLE IF NOT EXISTS journeys(tenancy_id TEXT PRIMARY KEY REFERENCES tenancies(id) ON DELETE CASCADE,payload TEXT NOT NULL)')
        db.execute("CREATE TABLE IF NOT EXISTS bills(id TEXT PRIMARY KEY,tenancy_id TEXT NOT NULL REFERENCES tenancies(id) ON DELETE CASCADE,provider TEXT NOT NULL,category TEXT NOT NULL,amount_cents INTEGER NOT NULL,due_date TEXT NOT NULL,paid INTEGER NOT NULL DEFAULT 0 CHECK(paid IN (0,1)),note TEXT NOT NULL DEFAULT '',created_at TEXT NOT NULL DEFAULT(strftime('%Y-%m-%dT%H:%M:%fZ','now')))")
    server=HTTPServer(('127.0.0.1',8000),Handler)
    print('RentRecord: http://127.0.0.1:8000 — Ctrl+C to stop',flush=True)
    webbrowser.open('http://127.0.0.1:8000')
    server.serve_forever()
