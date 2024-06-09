from app import db
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(200), unique=True)
    password = db.Column(db.String(200))
    is_active = db.Column(db.Boolean(), default=True)

    def __str__(self):
        return self.login

    def check_password(self, password):
        if self.password == password:
            return True
        return False



class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200))
    description = db.Column(db.String(255))
    author = db.Column(db.Integer)

    def __str__(self):
        return self.title