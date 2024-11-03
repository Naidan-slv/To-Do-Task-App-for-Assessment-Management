from app import db

class Tasks(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    assesement_title = db.Column(db.String(100), nullable=False)
    module_code = db.Column(db.String(8), nullable=False)
    deadline = db.Column(db.Date, nullable=False)
    description = db.Column(db.String(200), nullable=False)
    completed = db.Column(db.Boolean, nullable=True)

# in the code above we have created a class called Tasks which inherits from db.Model. This lets us use the SQLAlchemy ORM to interact with the database. We have also defined the columns of the table in the database. The id column is the primary key and is an integer. We can then connect this to our form so that the forms update the database.