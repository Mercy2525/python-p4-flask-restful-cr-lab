#!/usr/bin/env python3

from flask import Flask, jsonify, request, make_response
from flask_migrate import Migrate
from flask_restful import Api, Resource

from models import db, Plant

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///plants.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = True

migrate = Migrate(app, db)
db.init_app(app)

api = Api(app)

class Plants(Resource):
    def get(self):
        plants=[plant.to_dict() for plant in Plant.query.all()]

        response=make_response(jsonify(plants))
        return response
    
    def post(self):

        new_plant=Plant(
            id=request.data.get('id'),
            name=request.data.get('name'),
            image=request.data.get('image'),
            price=request.data.get('price')
        )

        db.session.add(new_plant)
        db.session.commit()

        plant_dict=new_plant.to_dict()

        response=make_response(jsonify(plant_dict),201)
        response.content_type='application/json'

        return response

api.add_resource(Plants,'/plants')


class PlantByID(Resource):
    def get(self,id):
        plant= Plant.query.filter_by(id=id).first()

        if plant is None:
            return {'error': 'Plant not found'}, 404    
        
     
        plant_dict=plant.to_dict()
        response=make_response(jsonify(plant_dict),200)
        return response
api.add_resource(PlantByID,'/plants/<int:id>')

if __name__ == '__main__':
    app.run(port=5555, debug=True)
