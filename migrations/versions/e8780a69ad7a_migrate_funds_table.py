"""migrate_funds_table

Revision ID: e8780a69ad7a
Revises: 
Create Date: 2024-08-27 03:15:01.557095

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'e8780a69ad7a'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('funds',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('uuid', mysql.CHAR(length=36), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.Column('fund_house', sa.String(length=255), nullable=False),
    sa.Column('nav', sa.Float(), nullable=False),
    sa.Column('performance_percentage', sa.Float(), nullable=False),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('deleted_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('funds')
    # ### end Alembic commands ###
