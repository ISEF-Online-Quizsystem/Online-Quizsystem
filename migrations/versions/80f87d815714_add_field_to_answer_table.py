"""add field to Answer table

Revision ID: 80f87d815714
Revises: 0ee7a876ffa2
Create Date: 2020-06-23 16:47:29.062467

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '80f87d815714'
down_revision = '0ee7a876ffa2'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('answer', sa.Column('right_choice', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('answer', 'right_choice')
    # ### end Alembic commands ###