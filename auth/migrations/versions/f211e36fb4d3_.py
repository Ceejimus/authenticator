"""empty message

Revision ID: f211e36fb4d3
Revises: None
Create Date: 2016-03-27 19:45:58.785835

"""

# revision identifiers, used by Alembic.
revision = 'f211e36fb4d3'
down_revision = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('salt', sa.String(), nullable=True))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'salt')
    ### end Alembic commands ###