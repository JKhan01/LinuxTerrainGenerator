from run import app,db
class model(db.Model):
    __tablename__ = "userCred"
    name = db.Column(db.varchar(15),nullable=False)
    emailID = db.Column(db.varchar(30),nullable=False,primary_key=True)
    password = db.Column(db.varchar(10), nullable=False)
    