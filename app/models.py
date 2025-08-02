from . import db

class QueryLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    case_type = db.Column(db.String(50))
    case_number = db.Column(db.String(50))
    filing_year = db.Column(db.String(10))
    timestamp = db.Column(db.DateTime, server_default=db.func.now())
    raw_response = db.Column(db.Text)
    status = db.Column(db.String(20))
