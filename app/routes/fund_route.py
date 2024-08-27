from flask import Blueprint, request, jsonify
from marshmallow import ValidationError
from datetime import datetime
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
        
    db.session.add(fund)
    db.session.commit()

    return jsonify(schema.dump(fund)), 201

# GET FUND BY ID
@fund_bp.route('/funds/<string:uuid>', methods=['GET'])
def get_fund(uuid):
    fund = Fund.query.filter_by(uuid=uuid).first()
    
    if fund is None:
        return jsonify({"error": "Fund not found"}), 404
    
    schema = FundSchema()
    
    return jsonify(schema.dump(fund))

# UPDATE FUND
@fund_bp.route('/funds/<string:uuid>', methods=['PUT'])
def update_fund(uuid):
    fund = Fund.query.filter_by(uuid=uuid).first()
    
    if fund is None:
        return jsonify({"error": "Fund not found"}), 404
    
    schema = FundSchema()
    
    try:
        fund_data = schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    fund.name = fund_data.name
    fund.fund_house = fund_data.fund_house
    fund.description = fund_data.description
    fund.nav = fund_data.nav
    fund.performance_percentage = fund_data.performance_percentage
    
    db.session.commit()

    return jsonify(schema.dump(fund))

# SOFT DELETE FUND
@fund_bp.route('/funds/<string:uuid>', methods=['DELETE'])
def delete_fund(uuid):
    fund = Fund.query.filter_by(uuid=uuid, deleted_at=None).first()
    
    if fund is None:
        return jsonify({"error": "Fund not found"}), 404
    
    fund.deleted_at = datetime.now()
    db.session.commit()

    return jsonify({}), 200
