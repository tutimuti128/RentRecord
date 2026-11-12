"""B1 foundation. Actor IDs must come from trusted server authentication."""
import sqlite3
from pathlib import Path

def database():
    db = sqlite3.connect(':memory:')
    db.executescript(Path(__file__).with_name('schema.sql').read_text())
    return db

def owned_tenancy(db, actor_id, tenancy_id):
    row = db.execute('SELECT * FROM tenancies WHERE id=? AND owner_id=?', (tenancy_id, actor_id)).fetchone()
    if row is None:
        raise PermissionError('Tenancy unavailable')
    return row

if __name__ == '__main__':
    db = database()
    db.execute("INSERT INTO users VALUES ('demo','Demo Tenant','tenant@example.test','tenant')")
    db.execute("INSERT INTO tenancies(id,owner_id,address,landlord_name,landlord_email,rent_cents,deposit_cents,start_date) VALUES ('home','demo','Example Street 1','Demo Landlord','landlord@example.test',80000,160000,'2026-11-01')")
    assert owned_tenancy(db, 'demo', 'home')
    try:
        owned_tenancy(db, 'another-user', 'home')
        raise AssertionError('Ownership check failed')
    except PermissionError:
        pass
    try:
        db.execute("INSERT INTO deposit_events(id,tenancy_id,stage) VALUES ('bad','home','invalid')")
        raise AssertionError('Stage check failed')
    except sqlite3.IntegrityError:
        pass
    print('PASS: schema, owner lookup, cross-user denial, deposit stage constraint')
