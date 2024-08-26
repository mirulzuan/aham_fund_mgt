from flask import Blueprint, request, jsonify
from marshmallow import ValidationError
from app.models.fund import Fund
from app.schemas.fund_schema import FundSchema
from app.utils.db import db

from app.models.fund import Fund
from app.schemas.fund_schema import FundSchema

fund_bp = Blueprint('funds', __name__)

# GET ALL FUNDS
@fund_bp.route('/funds', methods=['GET'])
def get_funds():
    funds = Fund.query.all()
    return jsonify(FundSchema(many=True).dump(funds))

# CREATE FUND
@fund_bp.route('/funds', methods=['POST'])
def create_fund():
    schema = FundSchema()

    try:
        fund = schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    fund = Fund(**fund)
    
    db.session.add(fund)
    db.session.commit()

    return jsonify(schema.dump(fund)), 201

# GET FUND BY ID
@fund_bp.route('/funds/<int:id>', methods=['GET'])
def get_fund(id):
    fund = Fund.query.get(id)
    
    if fund is None:
        return jsonify({"error": "Fund not found"}), 404
    
    schema = FundSchema()
    
    return jsonify(schema.dump(fund))

# UPDATE FUND
@fund_bp.route('/funds/<int:id>', methods=['PUT'])
def update_fund(id):
    fund = Fund.query.get(id)
    
    if fund is None:
        return jsonify({"error": "Fund not found"}), 404
    
    schema = FundSchema()
    
    try:
        fund_data = schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    fund.name = fund_data['name']
    fund.fund_house = fund_data['fund_house']
    fund.description = fund_data['description']
    fund.nav = fund_data['nav']
    fund.performance_percentage = fund_data['performance_percentage']
    
    db.session.commit()

    return jsonify(schema.dump(fund))

# DESTROY FUND
@fund_bp.route('/funds/<int:id>', methods=['DELETE'])
def delete_fund(id):
    fund = Fund.query.get(id)
    
    if fund is None:
        return jsonify({"error": "Fund not found"}), 404
    
    db.session.delete(fund)
    db.session.commit()

    return jsonify({}), 200
