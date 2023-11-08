from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///flaskLearning.db'       #* This will be my db name
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Details(db.Model):
    __tablename__ = 'UserDetails'

    id = db.Column(db.Integer, primary_key = True)
    fName = db.Column(db.String(20), nullable = False)
    lName = db.Column(db.String(20), nullable = False)
    email = db.Column(db.String(30), unique = True,  nullable = False)
    password = db.Column(db.String(30), nullable = False)
    description = db.Column(db.String(200))
    dateCreated = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)


    def __repr__(self) -> str:
        return f"{self.fName} -- {self.lName}"


@app.route('/', methods = ['GET', 'POST'])
def hello_world():
    if request.method=='POST':

        #* Do not use this syntax ---->  username=request.form["username"]
        fName = request.form.get("fName") 
        lName = request.form.get("lName") 
        email = request.form.get("email") 
        password = request.form.get("password")
        description = request.form.get("description")
        #* below is attribute in HTML   i.e name = value i.e value from the above which is retrieved from the form.
        userDetails = Details(fName = fName, lName = lName, email = email, password = password, description = description)
        db.session.add(userDetails)
        db.session.commit()

        # print(request.form.get("lName"))

        return redirect('/')


        
    result = Details.query.all()

    return render_template('index.html', userDetails = result)

@app.route('/show')
def show():

    #* THe queries both below do the same thing.
    #? result = db.session.execute(db.select(Details)).scalars()
    result = Details.query.all()
    # print(result)
    for user in result:
        print(f"User ID: {user.id}, fName: {user.fName}, lName: {user.lName}, Email: {user.email}, password: {user.password}, description: {user.description}")

    return 'This is products page.'


@app.route('/delete/<int:id>')
def delete(id):
    recordToBeDeleted = Details.query.filter_by(id = id).first()
    db.session.delete(recordToBeDeleted)
    db.session.commit()
    return redirect('/')


@app.route('/update/<int:id>', methods = ['GET', 'POST'])
def update(id):
    if request.method == "POST":
        fName = request.form.get("fName") 
        lName = request.form.get("lName") 
        email = request.form.get("email") 
        password = request.form.get("password")
        description = request.form.get("description")

        userToUpdate = Details.query.filter_by(id = id).first()

        userToUpdate.fName = fName
        userToUpdate.lName = lName
        userToUpdate.email = email
        userToUpdate.password = password
        userToUpdate.description = description

        db.session.commit()

        return redirect('/')

    detailsToUpdate = Details.query.filter_by(id = id).first()
    return render_template('update.html', detailsToUpdate = detailsToUpdate)

if(__name__ == "__main__"):
    app.run(debug=True, port=8000)