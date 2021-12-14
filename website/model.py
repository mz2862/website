from . import db


class Incident(db.Model):
    __tablename__ = 'incident'
    id = db.Column(db.Integer, primary_key=True)
    incident_key = db.Column(db.String(), nullable=False)
    incident_type = db.Column(db.String(), nullable=False)  # shooting or arrest
    date = db.Column(db.Date(), nullable=False)  # datetime.date()`` objects.
    time = db.Column(db.Time(), nullable=True)  # datetime.time() object
    offense = db.Column(db.String(), nullable=True)
    borough = db.Column(db.String(), nullable=True)
    precinct = db.Column(db.String(), nullable=True)
    location_desc = db.Column(db.String(), nullable=True)
    latitude = db.Column(db.Float(), nullable=True)
    longitude = db.Column(db.Float(), nullable=True)
    perp_sex = db.Column(db.String(), nullable=True)
    perp_age_group = db.Column(db.String(), nullable=True)
    perp_race = db.Column(db.String(), nullable=True)
    vic_sex = db.Column(db.String(), nullable=True)
    vic_race = db.Column(db.String(), nullable=True)
    vic_age_group = db.Column(db.String(), nullable=True)

    def __repr__(self):
        return f"<INCIDENT {self.incident_key} : {self.incident_type}>"
