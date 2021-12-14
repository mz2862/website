### Import necessary packages

import pandas as pd
import numpy as np
# sqlalchemy The Database Toolkit for Python
from sqlalchemy import create_engine
# Establishing Connectivity
engine = create_engine('postgresql://postgres:123@localhost:5432/postgres')

import os
dir_path = os.path.dirname(os.path.realpath(__file__))
### Import Data
arrest_df = pd.read_csv( dir_path + "/data/NYPD_Arrest_Data__Year_to_Date_.csv")
shooting_incident_df = pd.read_csv(dir_path + "/data/NYPD_Shooting_Incident_Data__Year_To_Date_.csv")

### Data Preprocess
## convert datetime formate
arrest_df.ARREST_DATE = pd.to_datetime(arrest_df.ARREST_DATE).dt.date
shooting_incident_df.OCCUR_DATE = pd.to_datetime(shooting_incident_df.OCCUR_DATE).dt.date
shooting_incident_df.OCCUR_TIME = pd.to_datetime(shooting_incident_df.OCCUR_TIME, format='%H:%M:%S').dt.time


## drop dupilcates
arrest_df.drop_duplicates(inplace=True)
shooting_incident_df.drop_duplicates(inplace=True)

### fill missing value
arrest_df.fillna(np.nan, inplace=True)
for c in arrest_df.columns:
    arrest_df[c].fillna(np.nan, inplace=True)

shooting_incident_df.fillna(np.nan, inplace=True)
for c in shooting_incident_df.columns:
    shooting_incident_df[c].fillna(np.nan, inplace=True)


# using sqlalchemy.orm to declaree mapping model
from sqlalchemy.orm import declarative_base
Base = declarative_base()
from sqlalchemy import Column, Integer, String, Date, DateTime, Time, Float, Integer, ForeignKey
class Incident(Base):
    __tablename__ = 'incident'
    id = Column(Integer, primary_key=True)
    incident_key = Column(String(30), nullable=False, unique=True)
    incident_type = Column(String, nullable=False)  # shooting or arrest
    date = Column(Date, nullable=False)  # datetime.date()`` objects.
    time = Column(Time, nullable=True)  # datetime.time() object
    offense = Column(String(), nullable=True)
    borough = Column(String(), nullable=True)
    precinct = Column(String(), nullable=True)
    location_desc = Column(String(), nullable=True)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    perp_sex = Column(String(), nullable=True)
    perp_age_group = Column(String(), nullable=True)
    perp_race = Column(String(), nullable=True)
    vic_sex = Column(String(), nullable=True)
    vic_race = Column(String(), nullable=True)
    vic_age_group = Column(String(), nullable=True)

#This appends CASCADE to the DROP TABLE statement issued for the postgresql dialect while keeping all other dialects the same.
from sqlalchemy.schema import DropTable
from sqlalchemy.ext.compiler import compiles

@compiles(DropTable, "postgresql")
def _compile_drop_table(element, compiler, **kwargs):
    return compiler.visit_drop_table(element) + " CASCADE"

# drop if exists and create all
Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)


from sqlalchemy.orm import sessionmaker
Session = sessionmaker(bind = engine)
session = Session()

# incident
keys = []


def inserRowByShooting(row):
    if (row["INCIDENT_KEY"]) not in keys:
        keys.append(row["INCIDENT_KEY"])
        incident = Incident()
        incident.incident_key = row["INCIDENT_KEY"]
        incident.incident_type = "shooting"

        incident.date = row["OCCUR_DATE"]
        incident.time = row["OCCUR_TIME"]

        incident.borough = row["BORO"]
        incident.precinct = row["PRECINCT"]
        incident.location_desc = row["LOCATION_DESC"]

        incident.perp_sex = row["PERP_SEX"]
        incident.perp_age_group = row["PERP_AGE_GROUP"]
        incident.perp_race = row["PERP_RACE"]

        incident.vic_sex = row["VIC_SEX"]
        incident.vic_race = row["VIC_RACE"]
        incident.vic_age_group = row["VIC_AGE_GROUP"]

        incident.latitude = row["Latitude"]
        incident.longitude = row["Longitude"]

        session.add(incident)
        session.commit()


def inserRowByArrest(row):
    if (row["ARREST_KEY"]) not in keys:
        keys.append(row["ARREST_KEY"])
        incident = Incident()
        incident.incident_key = row["ARREST_KEY"]
        incident.incident_type = "arrest"
        incident.date = row["ARREST_DATE"]
        incident.offense = row["OFNS_DESC"]
        incident.borough = row["ARREST_BORO"]
        incident.precinct = row["ARREST_PRECINCT"]

        incident.perp_sex = row["PERP_SEX"]
        incident.perp_age_group = row["AGE_GROUP"]
        incident.perp_race = row["PERP_RACE"]

        incident.latitude = row["Latitude"]
        incident.longitude = row["Longitude"]

        session.add(incident)
        session.commit()

shooting_incident_df.apply(lambda row: inserRowByShooting(row), axis=1)
arrest_df.apply(lambda row: inserRowByArrest(row), axis=1)