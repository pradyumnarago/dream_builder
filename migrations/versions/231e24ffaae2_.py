"""empty message

Revision ID: 231e24ffaae2
Revises: 89df195cfa9e
Create Date: 2024-12-20 13:29:32.451400

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '231e24ffaae2'
down_revision = '89df195cfa9e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.add_column(sa.Column('reset_token', sa.String(length=255), nullable=True))
        batch_op.add_column(sa.Column('reset_token_expiration', sa.DateTime(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.drop_column('reset_token_expiration')
        batch_op.drop_column('reset_token')

    # ### end Alembic commands ###
