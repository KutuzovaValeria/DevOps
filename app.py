from flask import Flask, request, jsonify, render_template
from flask_migrate import Migrate
from extensions import db
from models import Incident, Person, IncidentPerson

app = Flask(__name__)
app.config.from_pyfile('config.py')

db.init_app(app)
migrate = Migrate(app, db)

@app.route('/')
def index():
    return render_template('index.html', title="Главная страница")

@app.route('/incidents_count', methods=['GET'])
def get_incidents_count():
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    count = Incident.query.filter(
        Incident.registration_date.between(start_date, end_date)
    ).count()
    return render_template('/incidents_count', start_date=start_date, end_date=end_date, count=count)


@app.route('/person_incidents/<person_id>', methods=['GET'])
def get_person_incidents(person_id):
    count = IncidentPerson.query.filter_by(person_id=person_id).count()
    return jsonify({'person_incident_count': count})

@app.route('/incident', methods=['POST'])
def add_incident():
    data = request.json
    new_incident = Incident(
        registration_number=data['registration_number'],
        registration_date=data['registration_date'],
        summary=data['summary'],
        decision=data['decision']
    )
    db.session.add(new_incident)
    db.session.commit()
    return jsonify({'message': 'Incident added successfully'})

@app.route('/incident/<int:incident_id>', methods=['PUT'])
def update_incident(incident_id):
    data = request.json
    incident = Incident.query.get_or_404(incident_id)
    incident.registration_number = data['registration_number']
    incident.registration_date = data['registration_date']
    incident.summary = data['summary']
    incident.decision = data['decision']
    db.session.commit()
    return jsonify({'message': 'Incident updated successfully'})

@app.route('/person', methods=['POST'])
def add_person():
    data = request.json
    new_person = Person(
        registration_number=data['registration_number'],
        last_name=data['last_name'],
        first_name=data['first_name'],
        middle_name=data.get('middle_name'),
        address=data['address'],
        convictions_count=data.get('convictions_count', 0)
    )
    db.session.add(new_person)
    db.session.commit()
    return jsonify({'message': 'Person added successfully'})

@app.route('/person/<int:person_id>', methods=['PUT'])
def update_person(person_id):
    data = request.json
    person = Person.query.get_or_404(person_id)
    person.registration_number = data['registration_number']
    person.last_name = data['last_name']
    person.first_name = data['first_name']
    person.middle_name = data.get('middle_name')
    person.address = data['address']
    person.convictions_count = data['convictions_count']
    db.session.commit()
    return jsonify({'message': 'Person updated successfully'})
