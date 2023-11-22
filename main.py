from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
import uuid

# Flask App Configuration
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://your_username:your_password@localhost/your_database'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Database Models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    unique_id = db.Column(db.String(80), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    city = db.Column(db.String(100), nullable=False)
    has_voted = db.Column(db.Boolean, default=False)

class Vote(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    choice = db.Column(db.String(80), nullable=False)

# Create Database Tables
db.create_all()

# Route for User Registration
@app.route('/register', methods=['POST'])
def register():
    data = request.json
    new_user = User(unique_id=str(uuid.uuid4()), name=data['name'], age=data['age'], city=data['city'], has_voted=False)
    db.session.add(new_user)
    db.session.commit()
    return {"message": "Registered successfully", "unique_id": new_user.unique_id}

# Route for Voting
@app.route('/vote', methods=['POST'])
def vote():
    unique_id = request.json.get('unique_id')
    choice = request.json.get('choice')

    user = User.query.filter_by(unique_id=unique_id).first()
    if user and not user.has_voted:
        new_vote = Vote(user_id=user.id, choice=choice)
        user.has_voted = True
        db.session.add(new_vote)
        db.session.commit()
        return {"message": "Vote recorded successfully"}
    else:
        return {"message": "Invalid ID or already voted"}, 400

# Application Entry Point
if __name__ == '__main__':
    app.run(debug=True)
