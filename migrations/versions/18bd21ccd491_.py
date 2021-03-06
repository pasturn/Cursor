"""empty message

Revision ID: 18bd21ccd491
Revises: 8cb560abfb1a
Create Date: 2016-08-31 12:48:05.043601

"""

# revision identifiers, used by Alembic.
revision = '18bd21ccd491'
down_revision = '8cb560abfb1a'

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('posts')
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('posts',
    sa.Column('id', mysql.INTEGER(display_width=11), nullable=False),
    sa.Column('title', mysql.VARCHAR(length=200), nullable=True),
    sa.Column('body', mysql.MEDIUMTEXT(), nullable=True),
    sa.Column('timestamp', mysql.DATETIME(), nullable=True),
    sa.Column('user_id', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.user_id'], name='posts_ibfk_1'),
    sa.PrimaryKeyConstraint('id'),
    mysql_default_charset='latin1',
    mysql_engine='InnoDB'
    )
    ### end Alembic commands ###
