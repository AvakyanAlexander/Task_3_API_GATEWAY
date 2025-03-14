"""init7

Revision ID: a10a7390f6e0
Revises: 23ee43f59de3
Create Date: 2025-03-10 16:05:17.418018

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'a10a7390f6e0'
down_revision: Union[str, None] = '23ee43f59de3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('contract_document',
    sa.Column('con_doc_id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('contract_id', sa.Integer(), nullable=False),
    sa.Column('document_id', sa.Integer(), nullable=False),
    sa.Column('date_bind', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['contract_id'], ['contract.con_id'], ),
    sa.ForeignKeyConstraint(['document_id'], ['documents.doc_id'], ),
    sa.PrimaryKeyConstraint('con_doc_id')
    )
    op.drop_table('contract_documents')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('contract_documents',
    sa.Column('contract_id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('document_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('con_doc_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('date_bind', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['contract_id'], ['contract.con_id'], name='contract_documents_contract_id_fkey'),
    sa.ForeignKeyConstraint(['document_id'], ['documents.doc_id'], name='contract_documents_document_id_fkey'),
    sa.PrimaryKeyConstraint('contract_id', name='contract_documents_pkey')
    )
    op.drop_table('contract_document')
    # ### end Alembic commands ###
