"""change fks on invitations table



Revision ID: c6a6f549e741
Revises: db06c6d168a2
Create Date: 2023-08-07 07:05:02.565806

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c6a6f549e741'
down_revision = 'db06c6d168a2'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('invitation', schema=None) as batch_op:
        batch_op.alter_column('sender_id',
               existing_type=sa.INTEGER(),
               type_=sa.String(length=255),
               existing_nullable=False)
        batch_op.alter_column('receiver_id',
               existing_type=sa.INTEGER(),
               type_=sa.String(length=255),
               existing_nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('invitation', schema=None) as batch_op:
        batch_op.alter_column('receiver_id',
               existing_type=sa.String(length=255),
               type_=sa.INTEGER(),
               existing_nullable=False)
        batch_op.alter_column('sender_id',
               existing_type=sa.String(length=255),
               type_=sa.INTEGER(),
               existing_nullable=False)

    # ### end Alembic commands ###