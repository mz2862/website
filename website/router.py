from flask import render_template
import sqlalchemy as sa
from . import app, db
from .model import Incident

# query arrest data and shooting data while starting the app, then we can use them later
ArrestDateQuery = Incident.query.filter_by(incident_type="arrest").order_by(Incident.date).all()
ArrestData = Incident.query.filter_by(incident_type="arrest").all()

ShootingDateQuery = Incident.query.filter_by(incident_type="shooting").order_by(Incident.date).all()
ShootingData = Incident.query.filter_by(incident_type="shooting").all()

#  home page router
@app.route('/')
def index():
    data = []
    # query all data by type
    result = db.session.query(Incident.incident_type, sa.func.count()).group_by(Incident.incident_type).all()
    for r in result:
        if r[0] == "arrest":
            data.append({"type": r[0], "records": r[1], "start": ArrestData[-1].date, "end":ArrestData[0].date})
        else:
            data.append({"type": r[0], "records": r[1],  "start":ShootingData[-1].date  , "end":ShootingData[0].date})

    return render_template("index.html", data=data)


@app.route('/shootingByMap')
def shootingByMap():
    # query all data by shooting
    shootings = Incident.query.filter_by(incident_type="shooting").all()
    dateQuery = Incident.query.filter_by(incident_type="shooting").order_by(Incident.date).all()
    # form result, and pass them into template
    start_date = dateQuery[0].date
    end_date = dateQuery[-1].date
    result = []
    for s in shootings:
        if s.location_desc:
            locationDesc = s.location_desc
        else:
            locationDesc = "None"

        result.append([locationDesc, s.latitude, s.longitude])

    return render_template("shootingByMap.html", result=result, start_date=start_date, end_date=end_date)


@app.route("/shootingByBoro")
def shootingByBoro():
    # query all data by shooting
    dateQuery = Incident.query.filter_by(incident_type="shooting").order_by(Incident.date).all()
    start_date = dateQuery[0].date
    end_date = dateQuery[-1].date
    # group shooting data by borough
    shootings = db.session.query(Incident.borough, sa.func.count()).filter_by(incident_type="shooting").group_by(
        Incident.borough).all()
    # form result, and pass them into template
    data = []
    labels = []
    for a, b in shootings:
        labels.append(a)
        data.append(b)

    return render_template("shootingByBoro.html", data=data, labels=labels,  start_date=start_date, end_date=end_date)


@app.route("/shootingByMonth")
def shootingByMonth():
    # query all data by shooting and order by date
    dateQuery = Incident.query.filter_by(incident_type="shooting").order_by(Incident.date).all()
    start_date = dateQuery[0].date
    end_date = dateQuery[-1].date
    # group shooting data by month
    month = sa.func.date_trunc('month', Incident.date)
    result = db.session.query(month, sa.func.count()).filter_by(incident_type="shooting"). \
        group_by(month).order_by(month).all()
    # form result, and pass them into template
    data = []
    labels = []
    for r in result:
        data.append(r[1])
        labels.append(r[0].strftime("%m/%d/%Y"))

    return render_template("shootingByMonth.html", data=data, labels=labels, start_date=start_date, end_date=end_date)


@app.route("/arrestByBoro")
def arrestByBoro():
    start_date = ArrestDateQuery[0].date
    end_date = ArrestDateQuery[-1].date
    # group arrest data by borough
    arrests = db.session.query(Incident.borough, sa.func.count()).filter_by(incident_type="arrest").group_by(
        Incident.borough).all()
    # form result, and pass them into template
    data = []
    labels = []
    label_dict = {"Q": "QUEENS", "B": "BRONX", "S": "STATEN ISLAND ", "K": "BROOKLYN", "M": "MANHATTAN"}
    for a, b in arrests:
        labels.append(label_dict[a])
        data.append(b)
    return render_template("arrestByBoro.html", data=data,labels=labels, start_date=start_date, end_date=end_date)


@app.route("/arrestByMonth")
def arrestByMonth():
    start_date = ArrestDateQuery[0].date
    end_date = ArrestDateQuery[-1].date
    # group arrest data by month
    month = sa.func.date_trunc('month', Incident.date)
    result = db.session.query(month, sa.func.count()).filter_by(incident_type="arrest"). \
        group_by(month).order_by(month).all()
    # form result, and pass them into template
    data = []
    labels = []
    for r in result:
        data.append(r[1])
        labels.append(r[0].strftime("%m/%d/%Y"))
    return render_template("arrestByMonth.html", data=data, labels=labels, start_date=start_date, end_date=end_date)


@app.route("/arrestBySex")
def arrestBySex():
    start_date = ArrestDateQuery[0].date
    end_date = ArrestDateQuery[-1].date
    # group arrest data by perp_sex
    arrests = db.session.query(Incident.perp_sex, sa.func.count()).filter_by(incident_type="arrest").group_by(
        Incident.perp_sex).all()
    # form result, and pass them into template

    labels = []
    data = []
    for a, b in arrests:
        data.append(b)
        labels.append(a)

    return render_template("arrestBySex.html", data=data, labels=labels, start_date=start_date, end_date=end_date)


@app.route("/arrestByRace")
def arrestByRace():
    start_date = ArrestDateQuery[0].date
    end_date = ArrestDateQuery[-1].date

    # group arrest data by perp_race
    arrests = db.session.query(Incident.perp_race, sa.func.count()).filter_by(incident_type="arrest").group_by(
        Incident.perp_race).all()
    # form result, and pass them into template

    labels = []
    data = []
    for a, b in arrests:
        data.append(b)
        labels.append(a)

    return render_template("arrestByRace.html", data=data, labels=labels, start_date=start_date, end_date=end_date)


@app.route("/arrestByAgeGroup")
def arrestByAgeGroup():
    start_date = ArrestDateQuery[0].date
    end_date = ArrestDateQuery[-1].date
    # group arrest data by perp_age_group
    arrests = db.session.query(Incident.perp_age_group, sa.func.count()).filter_by(incident_type="arrest").group_by(
        Incident.perp_age_group).all()
    # form result, and pass them into template

    labels = []
    data = []
    for a, b in arrests:
        data.append(b)
        labels.append(a)

    return render_template("arrestByAgeGroup.html", data=data, labels=labels, start_date=start_date, end_date=end_date)