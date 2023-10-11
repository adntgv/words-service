"""create words table

Revision ID: dc0c61b08f4a
Revises: 
Create Date: 2023-10-11 17:14:14.146599

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'dc0c61b08f4a'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    # Create words table
    op.create_table(
        'words',
        sa.Column('word_id', sa.Integer, primary_key=True, index=True),
        sa.Column('word_text', sa.String, unique=True, index=True),
        sa.Column('date_added', sa.Date)
    )

    # Create definitions table
    op.create_table(
        'definitions',
        sa.Column('definition_id', sa.Integer, primary_key=True),
        sa.Column('word_id', sa.Integer, sa.ForeignKey('words.word_id')),
        sa.Column('definition_text', sa.Text),
        sa.Column('example_text', sa.Text)
    )

    # Create translations table
    op.create_table(
        'translations',
        sa.Column('translation_id', sa.Integer, primary_key=True),
        sa.Column('word_id', sa.Integer, sa.ForeignKey('words.word_id')),
        sa.Column('translated_text', sa.Text),
        sa.Column('language', sa.String)
    )

    # Create synonyms table
    op.create_table(
        'synonyms',
        sa.Column('synonym_id', sa.Integer, primary_key=True),
        sa.Column('translation_id', sa.Integer, sa.ForeignKey('translations.translation_id')),
        sa.Column('synonym_text', sa.Text)
    )

def downgrade() -> None:
    # Drop tables in reverse order of creation
    op.drop_table('synonyms')
    op.drop_table('translations')
    op.drop_table('definitions')
    op.drop_table('words')
