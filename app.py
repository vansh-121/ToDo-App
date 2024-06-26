from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///project.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Vansh(db.Model):
    sno = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String, nullable = False)
    details = db.Column(db.String, nullable = False)
    date = db.Column(db.DateTime, default = datetime.utcnow)

    def __repr__(self) -> str:
        return f" {self.name} - {self.date}"

@app.route('/', methods = ['GET', 'POST'])
def hello_world():
    if request.method == 'POST':
        name = request.form['name']
        details = request.form['details']
        vansh = Vansh(name = name, details = details)
        db.session.add(vansh)
        db.session.commit()
    allvansh = Vansh.query.all()
    # print(allvansh)
    return render_template('index.html', allvansh = allvansh)

@app.route('/show')
def product():
    allvansh = Vansh.query.all()
    # print(allvansh)
    return "Product Page"

@app.route('/update/<int:sno>', methods = ['GET', 'POST'])
def update(sno):
    if request.method == 'POST':
        name = request.form['name']
        details = request.form['details']
        vansh = Vansh.query.filter_by(sno=sno).first()
        vansh.name = name
        vansh.details = details
        db.session.add(vansh)
        db.session.commit()
        return redirect('/')
    allvansh = Vansh.query.filter_by(sno=sno).first()
    # print(allvansh)
    return render_template('update.html', allvansh = allvansh)

@app.route('/delete/<int:sno>')
def delete(sno):
    allvansh = Vansh.query.filter_by(sno=sno).first()
    db.session.delete(allvansh)
    db.session.commit()
    # print(allvansh)
    return redirect('/')      

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=2000)