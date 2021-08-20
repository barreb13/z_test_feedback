from typing import final
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
#from send_mail import send_mail

app = Flask(__name__)
ENV = 'dev'

if ENV == 'dev':
    #db
    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:'password'@localhost/Ziply' # 'password' = password
else:
    #production db
    app.debug =False
    app.config['SQLALCHEMY_DATABASE_URI'] = ''

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db = SQLAlchemy(app)

class Feedback1(db.Model):
    __tablename__ = 'feedback1'
    id = db.Column(db.Integer, primary_key = True)
    techEmail = db.Column(db.String(200), unique=True)
    techName = db.Column(db.String(200))
    understandingProduct = db.Column(db.Integer)
    understandingProcess = db.Column(db.Integer)
    wasValuable = db.Column(db.Integer)
    wasOrganized = db.Column(db.Integer)
    metExpectations = db.Column(db.Integer)
    trainingProficiency = db.Column(db.String(200))
    trainingPace = db.Column(db.String(200))
    bestFormat = db.Column(db.String(200))
    commentsImproved = db.Column(db.Text())
    overall = db.Column(db.Integer)
    finalComments = db.Column(db.Text())


    def __init__(self, techEmail, techName, understandingProduct, understandingProcess, wasValuable, 
                    wasOrganized, metExpectations, trainingProficiency,
                    trainingPace, bestFormat, commentsImproved, overall, finalComments):
        self.techEmail = techEmail
        self.techName = techName
        self.understandingProduct = understandingProduct
        self.understandingProcess = understandingProcess
        self.wasValuable = wasValuable
        self.wasOrganized = wasOrganized
        self.metExpectations = metExpectations
        self.trainingProficiency = trainingProficiency
        self.trainingPace = trainingPace
        self.bestFormat = bestFormat
        self.commentsImproved = commentsImproved
        self.overall = overall
        self.finalComments = finalComments

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        techEmail = request.form['techEmail']
        techName = request.form['techName']
        understandingProduct = request.form['understandingProduct']
        understandingProcess = request.form['understandingProcess']
        wasValuable = request.form['wasValuable']
        wasOrganized = request.form['wasOrganized']
        metExpectations = request.form['metExpectations']
        trainingProficiency = request.form['trainingProficiency']
        trainingPace = request.form['trainingPace']
        bestFormat = request.form['bestFormat']
        commentsImproved = request.form['commentsImproved']
        overall = request.form['overall']
        finalComments = request.form['finalComments']
        #print(techName, techEmail, understandingProduct, finalComments)
        if techEmail == '' or techName == '':
            return render_template('index.html', message='Please Enter Required Fields')
        
        #check if count of techEmail is at 0
        if db.session.query(Feedback1).filter(Feedback1.techEmail == techEmail).count() == 0:
            data = Feedback1(techEmail, techName, understandingProduct, understandingProcess, wasValuable, 
                    wasOrganized, metExpectations, trainingProficiency,
                    trainingPace, bestFormat, commentsImproved, overall, finalComments)
            #add to session
            db.session.add(data)
            #actually put into database
            db.session.commit()
            return render_template('success.html')
        #else false
        return render_template('index.html', message='You have already submitted feedback')


@app.route('/home')
def home():
    return render_template('home.html')        


if __name__ == '__main__':
    app.run()