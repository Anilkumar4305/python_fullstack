from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Organization(db.Model):
    __tablename__ = 'organizations'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(200), nullable=True)
    users = db.relationship('User', backref='organization', lazy=True)

    def to_dict(self):
        return {"id": self.id, "name": self.name, "address": self.address}

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    organization_id = db.Column(db.Integer, db.ForeignKey('organizations.id'), nullable=False)

    def to_dict(self):
        return {"id": self.id, "name": self.name, "email": self.email, "organization_id": self.organization_id}