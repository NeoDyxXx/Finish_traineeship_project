"""empty message

Revision ID: 844fe0e14cd6
Revises: 
Create Date: 2022-04-23 12:44:27.687380

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '844fe0e14cd6'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('Country',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('Visa_Application_Centre',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('country_id', sa.Integer(), nullable=True),
    sa.Column('address', sa.String(length=200), nullable=True),
    sa.Column('email', sa.String(length=70), nullable=True),
    sa.Column('working_hours', sa.String(length=100), nullable=True),
    sa.Column('phone1', sa.String(length=20), nullable=True),
    sa.Column('phone2', sa.String(length=20), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('country')
    op.drop_table('news_details')
    op.drop_table('visa_application_centre')
    op.drop_table('news')
    op.drop_table('consulate')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('consulate',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('country_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('address', sa.VARCHAR(length=200), autoincrement=False, nullable=True),
    sa.Column('email', sa.VARCHAR(length=70), autoincrement=False, nullable=True),
    sa.Column('working_hours', sa.VARCHAR(length=100), autoincrement=False, nullable=True),
    sa.Column('phone_number_1', sa.VARCHAR(length=20), autoincrement=False, nullable=True),
    sa.Column('phone_number_2', sa.VARCHAR(length=20), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['country_id'], ['country.id'], name='consulate_country_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='consulate_pkey')
    )
    op.create_table('news',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('country_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('news_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('date', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['country_id'], ['country.id'], name='news_country_id_fkey'),
    sa.ForeignKeyConstraint(['news_id'], ['news_details.id'], name='news_news_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='news_pkey')
    )
    op.create_table('visa_application_centre',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('country_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('address', sa.VARCHAR(length=200), autoincrement=False, nullable=True),
    sa.Column('email', sa.VARCHAR(length=70), autoincrement=False, nullable=True),
    sa.Column('apply_working_hours', sa.VARCHAR(length=100), autoincrement=False, nullable=True),
    sa.Column('issue_working_hours', sa.VARCHAR(length=100), autoincrement=False, nullable=True),
    sa.Column('phone_number', sa.VARCHAR(length=20), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['country_id'], ['country.id'], name='visa_application_centre_country_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='visa_application_centre_pkey')
    )
    op.create_table('news_details',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('title', sa.VARCHAR(length=70), autoincrement=False, nullable=True),
    sa.Column('body', sa.VARCHAR(length=150), autoincrement=False, nullable=True),
    sa.Column('link', sa.VARCHAR(length=70), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='news_details_pkey')
    )
    op.create_table('country',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('name', sa.VARCHAR(length=50), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='country_pkey')
    )
    op.drop_table('Visa_Application_Centre')
    op.drop_table('Country')
    # ### end Alembic commands ###
