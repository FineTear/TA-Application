"""users table

Revision ID: 6027f4637452
Revises: 599909122d9b
Create Date: 2019-11-12 11:43:48.750444

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6027f4637452'
down_revision = '599909122d9b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('courses',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=140), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('courses')
    # ### end Alembic commands ###
