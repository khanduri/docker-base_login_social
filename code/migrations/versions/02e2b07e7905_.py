"""empty message

Revision ID: 02e2b07e7905
Revises: 
Create Date: 2018-04-29 19:05:21.046831

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '02e2b07e7905'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('Contact',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('created', sa.TIMESTAMP(), server_default=sa.text('now()'), nullable=True),
    sa.Column('removed_at', sa.TIMESTAMP(), nullable=True),
    sa.Column('updated', sa.TIMESTAMP(), server_default=sa.text('now()'), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('email', sa.String(length=63), nullable=True),
    sa.Column('name', sa.String(length=255), nullable=True),
    sa.Column('message', sa.String(length=1023), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('User',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('created', sa.TIMESTAMP(), server_default=sa.text('now()'), nullable=True),
    sa.Column('removed_at', sa.TIMESTAMP(), nullable=True),
    sa.Column('updated', sa.TIMESTAMP(), server_default=sa.text('now()'), nullable=True),
    sa.Column('email', sa.String(length=255), nullable=True),
    sa.Column('last_seen', sa.DateTime(), nullable=True),
    sa.Column('nickname', sa.String(length=63), nullable=True),
    sa.Column('about_me', sa.String(length=1023), nullable=True),
    sa.Column('timezone', sa.String(length=255), nullable=True),
    sa.Column('email_verification_token', sa.String(length=1023), nullable=True),
    sa.Column('admin', sa.Boolean(), nullable=True),
    sa.Column('email_verified', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email', 'removed_at', name='uix_email_rem')
    )
    op.create_table('UserSocial',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('created', sa.TIMESTAMP(), server_default=sa.text('now()'), nullable=True),
    sa.Column('removed_at', sa.TIMESTAMP(), nullable=True),
    sa.Column('updated', sa.TIMESTAMP(), server_default=sa.text('now()'), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('social_network', sa.String(length=63), nullable=False),
    sa.Column('social_id', sa.String(length=255), nullable=False),
    sa.Column('access_code', sa.String(length=2047), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('social_network', 'social_id', 'removed_at')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('UserSocial')
    op.drop_table('User')
    op.drop_table('Contact')
    # ### end Alembic commands ###