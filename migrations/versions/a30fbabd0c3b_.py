"""empty message

Revision ID: a30fbabd0c3b
Revises: fcfd895a76ff
Create Date: 2019-11-30 15:17:36.878221

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a30fbabd0c3b'
down_revision = 'fcfd895a76ff'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('course', sa.String(length=140), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'course')
    # ### end Alembic commands ###
