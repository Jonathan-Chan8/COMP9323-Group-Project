"""empty message

Revision ID: 3e9d7cc980ef
Revises: 
Create Date: 2021-08-02 19:47:31.889039

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3e9d7cc980ef'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(length=120), nullable=True),
    sa.Column('password', sa.VARCHAR(length=20), nullable=True),
    sa.Column('accountType', sa.Enum('client', 'guardian', name='account_type'), nullable=True),
    sa.Column('firstName', sa.VARCHAR(length=20), nullable=True),
    sa.Column('lastName', sa.VARCHAR(length=20), nullable=True),
    sa.Column('dateOfBirth', sa.Date(), nullable=True),
    sa.Column('age', sa.Integer(), nullable=True),
    sa.Column('gender', sa.Enum('male', 'female', 'other', name='gender_type'), nullable=True),
    sa.Column('contactNo', sa.VARCHAR(length=15), nullable=True),
    sa.Column('homeAddress', sa.VARCHAR(length=50), nullable=True),
    sa.Column('shortBio', sa.VARCHAR(length=140), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)
    op.create_table('clients',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('asGuardian', sa.BOOLEAN(), nullable=True),
    sa.Column('allergies', sa.VARCHAR(length=50), nullable=True),
    sa.Column('likes', sa.VARCHAR(length=50), nullable=True),
    sa.Column('dislikes', sa.VARCHAR(length=50), nullable=True),
    sa.Column('healthNeeds', sa.VARCHAR(length=50), nullable=True),
    sa.ForeignKeyConstraint(['id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('support_workers',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('languages', sa.VARCHAR(length=50), nullable=True),
    sa.Column('interests', sa.VARCHAR(length=50), nullable=True),
    sa.ForeignKeyConstraint(['id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('connected_users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('supportWorkerId', sa.Integer(), nullable=True),
    sa.Column('clientId', sa.Integer(), nullable=True),
    sa.Column('dateConnected', sa.Date(), nullable=True),
    sa.ForeignKeyConstraint(['clientId'], ['clients.id'], ),
    sa.ForeignKeyConstraint(['supportWorkerId'], ['support_workers.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('training',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('worker', sa.Integer(), nullable=True),
    sa.Column('subject', sa.VARCHAR(length=20), nullable=True),
    sa.Column('institution', sa.VARCHAR(length=20), nullable=True),
    sa.Column('startDate', sa.Date(), nullable=True),
    sa.Column('endDate', sa.Date(), nullable=True),
    sa.ForeignKeyConstraint(['worker'], ['support_workers.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('work_history',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('worker', sa.Integer(), nullable=True),
    sa.Column('location', sa.VARCHAR(length=50), nullable=True),
    sa.Column('startDate', sa.Date(), nullable=True),
    sa.Column('endDate', sa.Date(), nullable=True),
    sa.ForeignKeyConstraint(['worker'], ['support_workers.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('shifts',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('connectedId', sa.Integer(), nullable=True),
    sa.Column('shiftStatus', sa.BOOLEAN(), nullable=True),
    sa.Column('workerStatus', sa.BOOLEAN(), nullable=True),
    sa.Column('clientStatus', sa.BOOLEAN(), nullable=True),
    sa.Column('startTime', sa.TIMESTAMP(), nullable=True),
    sa.Column('endTime', sa.TIMESTAMP(), nullable=True),
    sa.Column('duration', sa.Interval(), nullable=True),
    sa.Column('frequency', sa.Enum('daily', 'weekly', 'fortnightly', 'monthly', name='frequencies'), nullable=True),
    sa.ForeignKeyConstraint(['connectedId'], ['connected_users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('activities',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('shift', sa.Integer(), nullable=True),
    sa.Column('location', sa.VARCHAR(length=50), nullable=True),
    sa.ForeignKeyConstraint(['shift'], ['shifts.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('reports',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('activity', sa.Integer(), nullable=True),
    sa.Column('mood', sa.Enum('angry', 'sad', 'moderate', 'happy', 'hyperactive', name='moods'), nullable=True),
    sa.Column('incident', sa.BOOLEAN(), nullable=True),
    sa.Column('incidentReport', sa.Text(), nullable=True),
    sa.Column('sessionReport', sa.Text(), nullable=True),
    sa.ForeignKeyConstraint(['activity'], ['activities.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('reports')
    op.drop_table('activities')
    op.drop_table('shifts')
    op.drop_table('work_history')
    op.drop_table('training')
    op.drop_table('connected_users')
    op.drop_table('support_workers')
    op.drop_table('clients')
    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.drop_table('users')
    # ### end Alembic commands ###
