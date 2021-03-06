"""empty message

Revision ID: f7f47b55b44c
Revises: 5ce15330b754
Create Date: 2019-12-03 10:39:25.024752

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f7f47b55b44c'
down_revision = '5ce15330b754'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_index(op.f('ix_user_username'), 'user', ['username'], unique=True)
    op.drop_index('ix_user_email', table_name='user')
    op.drop_column('user', 'gpa')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('gpa', sa.FLOAT(), nullable=True))
    op.create_index('ix_user_email', 'user', ['username'], unique=1)
    op.drop_index(op.f('ix_user_username'), table_name='user')
    # ### end Alembic commands ###
