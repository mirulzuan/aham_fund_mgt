from marshmallow import Schema, fields, validate, post_load
from app.models.fund import Fund

class FundSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    fund_house = fields.Str(required=True) # FM name -- ToDo: Create a separate schema for FM association
    description = fields.Str(allow_none=True)
    nav = fields.Float(required=True, validate=validate.Range(min=0))
    performance_percentage = fields.Float(required=True, validate=validate.Range(max=100))
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)

    @post_load
    def make_fund(self, data, **kwargs):
        return Fund(**data)
