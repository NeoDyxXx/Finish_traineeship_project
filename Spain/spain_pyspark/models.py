from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

db = SQLAlchemy()

class CountryModel(db.Model):
    __tablename__ = 'country'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))

    #centers = relationship(VisaCenterModel)

    def __init__(self, name):
        self.name = name

    # def __repr__(self):
    #     return f""

class VisaCenterModel(db.Model):
    __tablename__ = 'visa_application_centre'

    id = db.Column(db.Integer, primary_key=True)
    country_id = db.Column(db.Integer, ForeignKey("country.id"))
    address = db.Column(db.String(200))
    email = db.Column(db.String(70))
    apply_working_hours = db.Column(db.String(100))
    issue_working_hours = db.Column(db.String(100))
    phone_number = db.Column(db.String(20))

    country = relationship(CountryModel)

    def __init__(self, country_id, address, email, apply_working_hours, issue_working_hours, phone_number):
        self.country_id = country_id
        self.address = address
        self.email = email
        self.apply_working_hours = apply_working_hours
        self.issue_working_hours = issue_working_hours
        self.phone_number = phone_number

    # def __repr__(self):
    #     return f""

