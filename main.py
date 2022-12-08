# import library
from flask import Flask
from flask_restx import Resource, Api, reqparse
from flask_sqlalchemy import SQLAlchemy
import json

app = Flask(__name__)
api = Api(app)
db = SQLAlchemy()
db.init_app(app)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///stunting.db"


class Login(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False, unique=True)
    email = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)


@app.route("/database/create", methods=["GET"])
def createDatabase():
    with app.app_context():
        db.create_all()
        return "Database Created Successfully!"

@app.route("/stunting/all", methods=["GET"])
def getAllStudents():
    data_user = db.session.execute(db.select(Login).order_by(Login.usernmae)).scalars()
    data = []
    for users in data_user:
        data.append({
            'username': users.username,
            'email': users.email,
            'password': users.password,
        })
        return json.dumps(data)

# parser4Param = reqparse.RequestParser()
# parser4Param.add_argument('pertanyaan', type=str, help='Silahkan Bertanya')
parser4Body = reqparse.RequestParser()
parser4Body.add_argument('username', type=str, help='Masukkan Username', required=True)
parser4Body.add_argument('email', type=str, help='Masukkan Email', required=True)
parser4Body.add_argument('password', type=str, help='Masukkan Password', required=True)


@api.route('/stunting/Login/<string:username>')
class Login(Resource):

    # @api.expect(parser4Body)
    def get(self, username):
        userdata = db.session.execute(db.select(Login).filter_by(username=username)).first()
        if(userdata is None):
            return f"Data dengan username: {username} tidak ditemukan!"
        else:
            users=userdata[0]
            return{
                'METHOD': "GET",
                'id': users.id,
                'username': users.username,
                'email': users.email,
                'password': users.password,
                'status': 200,
            }

    # @api.route('/stunting/<string:username>/diagnosa/')
    # class diagnosa(Resource):
    #     def post(self):


@api.route('/stunting/')
class RegisterUser(Resource):
    @api.expect(parser4Body)
    def post(self):
        args = parser4Body.parse_args()
        Username = args['username']
        Email = args['email']
        Password = args['password']
        register = Login(
            username=Username,
            email=Email,
            password=Password
        )
        user = db.session.execute(db.select(Login).filter_by(username=Username)).first()
        if (user is not None):
            return f"Username: {Username} sudah digunakan!"
        else:
            db.session.add(register)
            db.session.commit()
            return {
                'Username': Username,
                'Email': Email,
                'Password': Password,
                'status': 200,
            }



if __name__ == '__main__':
    app.run(debug=True)
    createDatabase()
