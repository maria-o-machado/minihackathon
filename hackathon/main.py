from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
SQLALCHEMY_TRACK_MODIFICATIONS = False
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://username:password@localhost:server/db"
db = SQLAlchemy(app)
migrate = Migrate(app, db)

class Job(db.Model):
    __tablename__ = 'polls_job'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    limit_data = db.Column(db.Date())
    description = db.Column(db.String())
    type_of_job = db.Column(db.String())

    def __init__(self, name, limit_data, description, type_of_job):
        self.name = name
        self.limit_data = limit_data
        self.description = description
        self.type_of_job=type_of_job

@app.get('/jobs')
def returnjobs():
    result = {
        'result': [{"name": job.name, "limit_data": job.limit_data, "description": job.description, "type_of_job": job.type_of_job} for job in Job.query.all()]
    }
    return result

@app.get('/jobs/<id>')
def getjob(id):
    job = Job.query.get(id)
    if job is None:
        return "Job not found!\n", 404

    result = {"name": job.name, "limit_data": job.limit_data, "description": job.description,
                "type_of_job": job.type_of_job}

    return result


@app.post('/jobs')
def createnewjob():
    print(request.data)
    if request.is_json:
        data = request.get_json()
        new_job = Job(name=data['name'], limit_data=data['limit_data'], description=data['description'], type_of_job=data['type_of_job'])
        db.session.add(new_job)
        db.session.commit()
        return {"message": "Successfully added!\n"}
    else:
        return {"error": "The request is not in JSON format!\n"}

@app.put('/jobs/<id>')
def updatejobs(id):
    if request.is_json:
        data = request.get_json()
        job = Job.query.get(id)
        if job is None:
            return "Job not found!\n", 404

        job.name= data['name']
        job.limit_data = data['limit_data']
        job.description = data['description']
        job.type_of_job = data['type_of_job']
        db.session.commit()
        return {"message": "Succefully updated!\n"}
    else:
        return {"error": "The request is not in JSON format!\n"}

@app.delete('/jobs/<id>')
def deletejob(id):
    job = Job.query.get(id)
    if job is None:
        return "Job not found!\n", 404

    Job.query.filter_by(id=id).delete()
    db.session.commit()
    return 'Successfully deleted!\n'