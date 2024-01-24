from flask import Flask,request
from flask_sqlalchemy import SQLAlchemy



app=Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'

db=SQLAlchemy(app)
with app.app_context():
    class Drink(db.Model):
        id = db.Column(db.Integer,primary_key=True)
        name = db.Column(db.String(80),unique=True,nullable=False)
        description = db.Column(db.String(120))

        def __repr__(self):
            return f"{self.name} - {self.description}"


    @app.route('/')
    def index():
        return 'Hello!'

    @app.route('/drinks')
    def get_drinks():
        drinks = Drink.query.all()
        output=[]
        for drink in drinks:
            drink_data = {'name':drink.name,'description':drink.description}
            output.append(drink_data)
            print(output)
        return {"drinks":output}
    
    @app.route('/drinks/<id>')
    def get_drinks_with_id(id):
        drink = Drink.query.get_or_404(id)
        return {"name":drink.name,"description":drink.description}

    @app.route('/drink', methods=['POST'])
    def add_drink():
        drink=Drink(name=request.json['name'],description=request.json['description'])
        db.session.add(drink)
        db.session.commit()
        return {'id':drink.id}