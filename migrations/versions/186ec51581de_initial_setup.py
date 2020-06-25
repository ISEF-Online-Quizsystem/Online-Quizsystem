"""initial setup

Revision ID: 186ec51581de
Revises: 
Create Date: 2020-06-25 13:26:18.862082

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '186ec51581de'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('module',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=128), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_module_name'), 'module', ['name'], unique=True)
    op.create_table('question',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('question', sa.String(length=280), nullable=True),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.Column('module', sa.String(length=128), nullable=True),
    sa.Column('option_one', sa.String(length=128), nullable=True),
    sa.Column('option_two', sa.String(length=128), nullable=True),
    sa.Column('option_three', sa.String(length=128), nullable=True),
    sa.Column('option_four', sa.String(length=128), nullable=True),
    sa.Column('option_five', sa.String(length=128), nullable=True),
    sa.Column('right_choice', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_question_timestamp'), 'question', ['timestamp'], unique=False)
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=64), nullable=True),
    sa.Column('email', sa.String(length=120), nullable=True),
    sa.Column('password_hash', sa.String(length=128), nullable=True),
    sa.Column('about_me', sa.String(length=140), nullable=True),
    sa.Column('last_seen', sa.DateTime(), nullable=True),
    sa.Column('tutor', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_user_email'), 'user', ['email'], unique=True)
    op.create_index(op.f('ix_user_username'), 'user', ['username'], unique=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_user_username'), table_name='user')
    op.drop_index(op.f('ix_user_email'), table_name='user')
    op.drop_table('user')
    op.drop_index(op.f('ix_question_timestamp'), table_name='question')
    op.drop_table('question')
    op.drop_index(op.f('ix_module_name'), table_name='module')
    op.drop_table('module')
    # ### end Alembic commands ###
