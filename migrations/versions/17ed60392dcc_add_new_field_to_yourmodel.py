"""Add new_field to YourModel

Revision ID: 17ed60392dcc
Revises: 
Create Date: 2023-11-17 17:21:32.435178

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '17ed60392dcc'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('images', schema=None) as batch_op:
        batch_op.add_column(sa.Column('image_name', sa.String(length=255), nullable=True))
        batch_op.add_column(sa.Column('crop_image_name', sa.String(length=255), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('images', schema=None) as batch_op:
        batch_op.drop_column('crop_image_name')
        batch_op.drop_column('image_name')

    # ### end Alembic commands ###
