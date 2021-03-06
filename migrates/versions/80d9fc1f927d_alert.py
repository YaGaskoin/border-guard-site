"""alert

Revision ID: 80d9fc1f927d
Revises: 66f20daa6b67
Create Date: 2020-01-30 21:17:23.123225

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '80d9fc1f927d'
down_revision = '66f20daa6b67'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('alert',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('body', sa.Text(), nullable=True),
    sa.Column('created', sa.DateTime(), nullable=True),
    sa.Column('author', sa.String(length=100), nullable=True),
    sa.Column('slug', sa.String(length=200), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.add_column('photos', sa.Column('alert_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'photos', 'alert', ['alert_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'photos', type_='foreignkey')
    op.drop_column('photos', 'alert_id')
    op.drop_table('alert')
    # ### end Alembic commands ###
