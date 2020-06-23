"""remove forign key in question table

Revision ID: 72f45ee5e524
Revises: 80f87d815714
Create Date: 2020-06-23 16:58:04.998968

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '72f45ee5e524'
down_revision = '80f87d815714'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('question', sa.Column('module', sa.String(length=128), nullable=True))
    op.drop_constraint('FK__question__module__52593CB8', 'question', type_='foreignkey')
    op.drop_column('question', 'module_id')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('question', sa.Column('module_id', sa.INTEGER(), autoincrement=False, nullable=True))
    op.create_foreign_key('FK__question__module__52593CB8', 'question', 'module', ['module_id'], ['id'])
    op.drop_column('question', 'module')
    # ### end Alembic commands ###
